from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Seat, Booking, Payment, Ticket, ShowSeatPricing
from .serializers import (
    SeatSerializer,
    BookingSerializer,
    PaymentSerializer,
    TicketSerializer,
)
from .permissions import (
    IsRegularUser,
    IsBookingOwnerOrReadOnly,
    IsPaymentOwner,
    IsTicketOwner
)
from django.db.models import Q


# 🔹 List all available seats for a show
class SeatListView(generics.ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        show_id = self.kwargs['show_id']
        return Seat.objects.filter(show_id=show_id, is_booked=False)


# 🔹 Book seats for a show
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🔹 List all bookings by user
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


# 🔹 View/Update/Delete a single booking
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]


# 🔹 Create a payment for a booking
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaymentOwner]

    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']
        serializer.save(amount=booking.total_price)


# 🔹 View a specific payment
class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaymentOwner]


# 🔹 View user's tickets
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Ticket.objects.filter(booking__user=self.request.user)


# 🔹 Ticket detail
class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsTicketOwner]
