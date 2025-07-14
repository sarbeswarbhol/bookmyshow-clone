from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Seat, Booking, Payment, Ticket, ShowSeatPricing
from .serializers import (
    SeatSerializer,
    BookingSerializer,
    PaymentSerializer,
    TicketSerializer,
    ShowSeatPricingSerializer
)
from .permissions import (
    IsRegularUser,
    IsBookingOwnerOrReadOnly,
    IsPaymentOwner,
    IsTicketOwner
)
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
import uuid

# 🔹 List available seats for a show
class SeatListView(generics.ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        show_id = self.kwargs['show_id']
        return Seat.objects.filter(show_id=show_id, is_booked=False)


# 🔹 Create a booking
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🔹 List user bookings
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


# 🔹 Retrieve/Update/Delete a booking
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]


# 🔹 Create a payment (transaction_id auto-generated)
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# 🔹 View payment details
class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaymentOwner]


# 🔹 List user tickets
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Ticket.objects.filter(booking__user=self.request.user)


# 🔹 Ticket details
class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsTicketOwner]


# 🔹 List seat pricing for a show
class ShowSeatPricingListView(generics.ListAPIView):
    serializer_class = ShowSeatPricingSerializer

    def get_queryset(self):
        show_id = self.kwargs['show_id']
        return ShowSeatPricing.objects.filter(show_id=show_id)
