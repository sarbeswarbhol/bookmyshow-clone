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


# 🔹 Seat Serializer with dynamic price from context
class SeatSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'seat_type', 'screen', 'price']

    def get_price(self, obj):
        pricing_dict = self.context.get('pricing_dict', {})
        return pricing_dict.get(obj.seat_type, 0)


# 🔹 Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    seat = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['ticket_code', 'issued_at', 'qr_code', 'seat']

    def get_seat(self, obj):
        # Use pricing context to pass into seat serializer
        pricing_qs = ShowSeatPricing.objects.filter(show=obj.show)
        pricing_dict = {p.seat_type: p.price for p in pricing_qs}
        return SeatSerializer(obj.seat, context={'pricing_dict': pricing_dict}).data


# 🔹 Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all(), many=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'show', 'seats', 'total_price', 'created_at', 'status', 'tickets']
        read_only_fields = ['total_price', 'created_at', 'status', 'tickets']

    def validate(self, data):
        show = data['show']
        current_time = now()

        movie_duration = show.movie.duration or 0  # in minutes
        show_end_time = show.show_time + timedelta(minutes=movie_duration)

        if current_time > show_end_time:
            raise serializers.ValidationError("Cannot book tickets for a show that has already ended.")
        if current_time > show.show_time + timedelta(minutes=15):
            raise serializers.ValidationError("Bookings are closed 15 minutes after show starts.")
        if current_time < show.show_time - timedelta(days=2):
            raise serializers.ValidationError("Bookings open only within 2 days of show time.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        show = validated_data['show']
        seats = validated_data['seats']

        with transaction.atomic():
            # Lock seats
            locked_seats = Seat.objects.select_for_update().filter(id__in=[s.id for s in seats])

            errors = []
            for seat in locked_seats:
                if seat.screen != show.screen:
                    errors.append(f"Seat {seat.seat_number} does not belong to this screen.")
                # Booking overlap will be checked at booked seat level
                from .models import BookedSeat
                if BookedSeat.objects.filter(show=show, seat=seat).exists():
                    errors.append(f"Seat {seat.seat_number} is already booked for this show.")

            if errors:
                raise serializers.ValidationError({"seats": errors})

            # Price calculation
            pricing_qs = ShowSeatPricing.objects.filter(show=show)
            pricing_dict = {p.seat_type: p.price for p in pricing_qs}
            total_price = sum([pricing_dict.get(seat.seat_type, 0) for seat in locked_seats])

            # Create booking
            booking = Booking.objects.create(user=user, show=show, total_price=total_price)
            booking.seats.set(locked_seats)

            # Mark seats as booked for this show
            from .models import BookedSeat
            BookedSeat.objects.bulk_create([
                BookedSeat(show=show, seat=seat, booking=booking) for seat in locked_seats
            ])

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
        booking = validated_data.get('booking')

        if not booking:
            raise serializers.ValidationError("Booking is required.")

        if booking.user != user:
            raise serializers.ValidationError("You are not allowed to pay for this booking.")

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

        # ✅ Only allow 'success' or 'failed'
        if status not in ['success', 'failed']:
            raise serializers.ValidationError("Only 'success' or 'failed' status allowed.")

        # ✅ Prevent updates if already successful
        if instance.status == 'success':
            raise serializers.ValidationError("This payment is already marked as successful.")

        # ✅ Block payment if show has already started
        show_time = instance.booking.show.show_time
        if status == 'success' and now() > show_time:
            raise serializers.ValidationError("Cannot complete payment: the show has already started.")

        # ✅ Set status and paid time
        if status == 'success':
            instance.status = 'success'
            instance.paid_at = now()
        elif status == 'failed':
            instance.status = 'failed'

        instance.save()
        return instance

