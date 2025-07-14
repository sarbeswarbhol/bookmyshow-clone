from django.urls import path
from .views import (
    SeatListView,
    BookingCreateView, BookingListView, BookingDetailView,
    PaymentCreateView, PaymentDetailView,
    TicketListView, TicketDetailView,
    ShowSeatPricingListView, ShowSeatPricingCreateView, ShowSeatPricingUpdateView
)

urlpatterns = [
    # Seats
    path('seats/<int:show_id>/', SeatListView.as_view(), name='available-seats'),

    # Bookings
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # Payments
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),

    # Tickets
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

    # Seat Pricing
    path('pricing/<int:show_id>/', ShowSeatPricingListView.as_view(), name='show-seat-pricing'),
    path('pricing/create/', ShowSeatPricingCreateView.as_view(), name='show-seat-pricing-create'),
    path('pricing/<int:pk>/update/', ShowSeatPricingUpdateView.as_view(), name='show-seat-pricing-update'),
]
