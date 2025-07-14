from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
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
    IsTicketOwner,
    IsTheaterOwnerOfShowSeatPricing
)
from django.utils.timezone import now


# 🔹 List available seats for a show
class SeatListView(generics.ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        return Seat.objects.filter(show_id=self.kwargs['show_id'], is_booked=False)

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
        return Booking.objects.filter(user=self.request.user, is_cancelled=False)



# 🔹 Retrieve/Update/Delete a booking
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]


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
    permission_classes = [IsTheaterOwnerOfShowSeatPricing]

    def get_queryset(self):
        return ShowSeatPricing.objects.filter(show_id=self.kwargs['show_id'])


# 🔹 Create seat pricing
class ShowSeatPricingCreateView(generics.CreateAPIView):
    serializer_class = ShowSeatPricingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTheaterOwnerOfShowSeatPricing]

    def perform_create(self, serializer):
        serializer.save()


# 🔹 Update pricing
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
  
class PaymentUpdateView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaymentOwner]
    lookup_field = 'pk'
    
class BookingCancelView(APIView):
    permission_classes = [IsBookingOwnerOrReadOnly]

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
        booking.save()

        # Release booked seats
        for seat in booking.seats.all():
            seat.is_booked = False
            seat.save()

        return Response({"detail": "Booking cancelled and seats released."}, status=200)