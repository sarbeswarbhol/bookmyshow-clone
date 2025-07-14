from django.urls import path
from .views import (
    SeatListView,
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    PaymentCreateView,
    PaymentDetailView,
    TicketListView,
    TicketDetailView,
    ShowSeatPricingListView,
)

urlpatterns = [
    # 🔹 Seat-related
    path('shows/<int:show_id>/seats/', SeatListView.as_view(), name='seat-list'),

    # 🔹 Booking
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # 🔹 Payment
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),

    # 🔹 Ticket
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

    # 🔹 Seat Pricing
    path('shows/<int:show_id>/pricing/', ShowSeatPricingListView.as_view(), name='show-seat-pricing'),
]
