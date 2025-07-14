from django.urls import path
from .views import (
    SeatListView,
    BookingCreateView, BookingCancelView, BookingListView, BookingDetailView,
    PaymentCreateView, PaymentDetailView, PaymentUpdateView,
    TicketListView, TicketDetailView,
    ShowSeatPricingListView, ShowSeatPricingCreateView, ShowSeatPricingUpdateView
)

urlpatterns = [
    # Seats
    path('seats/<int:show_id>/', SeatListView.as_view(), name='available-seats'),

    # Bookings
    path('', BookingListView.as_view(), name='booking-list'),
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),

    # Payments
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),

    # Tickets
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

    # Seat Pricing
    path('pricing/<int:show_id>/', ShowSeatPricingListView.as_view(), name='show-seat-pricing'),
    path('pricing/create/', ShowSeatPricingCreateView.as_view(), name='show-seat-pricing-create'),
    path('pricing/<int:pk>/update/', ShowSeatPricingUpdateView.as_view(), name='show-seat-pricing-update'),
]
