from rest_framework import serializers
from .models import Seat, Booking, Payment, Ticket, ShowSeatPricing
from theaters.models import Show
from django.utils.timezone import now
from datetime import timedelta
from django.db import transaction
import uuid

# 🔹 Show Seat Pricing Serializer
class ShowSeatPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSeatPricing
        fields = ['id', 'show', 'seat_type', 'price']
        read_only_fields = []


# 🔹 Seat Serializer with optimized pricing
class SeatSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'seat_type', 'price', 'is_booked']

    def get_price(self, obj):
        pricing_dict = self.context.get('pricing_dict', {})
        return pricing_dict.get(obj.seat_type)


# 🔹 Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    seat = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['ticket_code', 'issued_at', 'qr_code', 'seat']

    def get_seat(self, obj):
        # Fetch all pricing for the show
        pricing_qs = ShowSeatPricing.objects.filter(show=obj.booking.show)
        pricing_dict = {p.seat_type: p.price for p in pricing_qs}

        # Serialize seat with pricing context
        return SeatSerializer(obj.seat, context={'pricing_dict': pricing_dict}).data



class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all(), many=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'show', 'seats', 'total_price', 'created_at', 'tickets']
        read_only_fields = ['total_price', 'created_at', 'tickets']

    def validate(self, data):
        show = data['show']
        current_time = now()

        # ✅ Dynamically calculate show end time from movie duration
        movie_duration = show.movie.duration or 0  # duration in minutes
        show_end_time = show.show_time + timedelta(minutes=movie_duration)

        if current_time > show_end_time:
            raise serializers.ValidationError("Cannot book tickets for a show that has already ended.")

        if current_time > show.show_time + timedelta(minutes=15):
            raise serializers.ValidationError("Bookings are closed 15 minutes after show starts.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        show = validated_data['show']
        seats = validated_data['seats']

        with transaction.atomic():
            locked_seats = Seat.objects.select_for_update().filter(id__in=[s.id for s in seats])

            errors = []
            for seat in locked_seats:
                if seat.show != show:
                    errors.append(f"Seat {seat.seat_number} does not belong to this show.")
                if seat.is_booked:
                    errors.append(f"Seat {seat.seat_number} is already booked.")
            if errors:
                raise serializers.ValidationError({"seats": errors})

            total_price = 0
            for seat in locked_seats:
                try:
                    price = ShowSeatPricing.objects.get(show=show, seat_type=seat.seat_type).price
                    total_price += price
                except ShowSeatPricing.DoesNotExist:
                    raise serializers.ValidationError(f"No pricing defined for seat type {seat.seat_type}.")

            booking = Booking.objects.create(user=user, show=show, total_price=total_price)
            booking.seats.set(locked_seats)

            for seat in locked_seats:
                seat.is_booked = True
                seat.save()
                
            for seat in locked_seats:
                Ticket.objects.create(booking=booking, seat=seat)

            return booking


# 🔹 Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'status', 'payment_method', 'transaction_id', 'paid_at']
        read_only_fields = ['amount', 'paid_at', 'transaction_id']
        extra_kwargs = {
            'booking': {'required': False},
            'payment_method': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        booking = validated_data['booking']

        # Booking must belong to user
        if booking.user != user:
            raise serializers.ValidationError("You are not allowed to pay for this booking.")

        # Prevent duplicate payments
        if Payment.objects.filter(booking=booking).exists():
            raise serializers.ValidationError("Payment already exists for this booking.")

        transaction_id = str(uuid.uuid4()).replace('-', '')[:12].upper()

        validated_data.pop('booking')
        return Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            transaction_id=transaction_id,
            **validated_data
        )
        
    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)

        if status not in ['success', 'failed']:
            raise serializers.ValidationError("Invalid status. Only 'success' or 'failed' allowed.")

        if status == 'success' and instance.status != 'success':
            instance.status = 'success'
            instance.paid_at = now()
        elif status == 'failed':
            instance.status = 'failed'

        instance.save()
        return instance

