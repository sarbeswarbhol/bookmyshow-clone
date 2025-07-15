from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Q

from .models import Seat, Booking, Payment, Ticket, ShowSeatPricing, BookedSeat
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
    IsTicketOwner,
    IsTheaterOwnerOfShowSeatPricing
)
from theaters.models import Show

# 🔹 List available seats for a show
class SeatListView(generics.ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        show = Show.objects.get(pk=self.kwargs['show_id'])
        booked_seat_ids = BookedSeat.objects.filter(show=show).values_list('seat_id', flat=True)
        return Seat.objects.filter(screen=show.screen).exclude(id__in=booked_seat_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        pricing_qs = ShowSeatPricing.objects.filter(show_id=self.kwargs['show_id'])
        context['pricing_dict'] = {p.seat_type: p.price for p in pricing_qs}
        return context


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
        return Booking.objects.filter(
            user=self.request.user,
            is_cancelled=False
        ).order_by('-created_at')


# 🔹 Retrieve/Update/Delete a booking
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]


# 🔹 Cancel a booking
class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=404)

        if booking.is_cancelled:
            return Response({"detail": "Booking already cancelled."}, status=400)

        if now() > booking.show.show_time:
            raise ValidationError("Cannot cancel booking after the show has started.")

        booking.is_cancelled = True
        booking.status = "cancelled"
        booking.save()

        # Release seats
        BookedSeat.objects.filter(booking=booking).delete()

        return Response({"detail": "Booking cancelled and seats released."}, status=200)


# 🔹 Create a payment
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


# 🔹 Update payment status
class PaymentUpdateView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaymentOwner]
    lookup_field = 'pk'


# 🔹 List user tickets
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Ticket.objects.filter(booking__user=self.request.user)


# 🔹 Retrieve individual ticket
class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsTicketOwner]


# 🔹 List seat pricing for a show
class ShowSeatPricingListView(generics.ListAPIView):
    serializer_class = ShowSeatPricingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTheaterOwnerOfShowSeatPricing]

    def get_queryset(self):
        return ShowSeatPricing.objects.filter(show_id=self.kwargs['show_id'])


# 🔹 Create seat pricing for a show
class ShowSeatPricingCreateView(generics.CreateAPIView):
    serializer_class = ShowSeatPricingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTheaterOwnerOfShowSeatPricing]

    def perform_create(self, serializer):
        serializer.save()


# 🔹 Update seat pricing
class ShowSeatPricingUpdateView(generics.UpdateAPIView):
    queryset = ShowSeatPricing.objects.all()
    serializer_class = ShowSeatPricingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTheaterOwnerOfShowSeatPricing]
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        if obj.show.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to update this seat pricing.")
        return obj
