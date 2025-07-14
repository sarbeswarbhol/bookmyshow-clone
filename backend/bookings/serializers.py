from rest_framework import serializers
from .models import Seat, Booking, Payment, Ticket, ShowSeatPricing
from theaters.models import Show
from django.utils.timezone import now
from datetime import timedelta
import uuid

# 🔹 Show Seat Pricing Serializer
class ShowSeatPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSeatPricing
        fields = ['id', 'show', 'seat_type', 'price']


# 🔹 Seat Serializer
class SeatSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'seat_type', 'price', 'is_booked']

    def get_price(self, obj):
        try:
            return ShowSeatPricing.objects.get(show=obj.show, seat_type=obj.seat_type).price
        except ShowSeatPricing.DoesNotExist:
            return None


# 🔹 Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    seat = SeatSerializer()

    class Meta:
        model = Ticket
        fields = ['ticket_code', 'issued_at', 'qr_code', 'seat']


# 🔹 Booking Serializer
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

        if current_time > show.end_time:
            raise serializers.ValidationError("Cannot book tickets for a show that has already ended.")

        if current_time > show.show_time + timedelta(minutes=15):
            raise serializers.ValidationError("Bookings are closed 15 minutes after show starts.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        show = validated_data['show']
        seats = validated_data['seats']

        # Check seat validity
        for seat in seats:
            if seat.show != show:
                raise serializers.ValidationError(f"Seat {seat.seat_number} does not belong to this show.")
            if seat.is_booked:
                raise serializers.ValidationError(f"Seat {seat.seat_number} is already booked.")

        # Calculate total price dynamically
        total_price = 0
        for seat in seats:
            try:
                price = ShowSeatPricing.objects.get(show=show, seat_type=seat.seat_type).price
                total_price += price
            except ShowSeatPricing.DoesNotExist:
                raise serializers.ValidationError(f"No pricing defined for seat type {seat.seat_type} in this show.")

        # Create booking
        booking = Booking.objects.create(user=user, show=show, total_price=total_price)
        booking.seats.set(seats)

        # Mark seats as booked
        Seat.objects.filter(id__in=[seat.id for seat in seats]).update(is_booked=True)

        return booking


# 🔹 Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'status', 'payment_method', 'transaction_id', 'paid_at']
        read_only_fields = ['amount', 'status', 'paid_at', 'transaction_id']

    def create(self, validated_data):
        booking = validated_data['booking']
        transaction_id = str(uuid.uuid4()).replace('-', '')[:12].upper()
        return Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            transaction_id=transaction_id,
            **validated_data
        )

    def update(self, instance, validated_data):
        # Only allow updating status to 'success' or 'failed'
        status = validated_data.get('status')
        if status and status not in ['success', 'failed']:
            raise serializers.ValidationError("Invalid status. Only 'success' or 'failed' allowed.")

        if status == 'success' and instance.status != 'success':
            instance.status = 'success'
            instance.paid_at = now()
        elif status == 'failed':
            instance.status = 'failed'

        instance.save()
        return instance
