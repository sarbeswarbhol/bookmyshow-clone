from django.contrib import admin
from .models import Seat, Booking, Payment, Ticket, ShowSeatPricing


@admin.register(ShowSeatPricing)
class ShowSeatPricingAdmin(admin.ModelAdmin):
    list_display = ('show', 'seat_type', 'price')
    list_filter = ('seat_type', 'show__theater', 'show__movie')
    search_fields = ('show__movie__title', 'show__theater__name')
    ordering = ('show', 'seat_type')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'seat_type', 'show', 'is_booked')
    list_filter = ('seat_type', 'is_booked', 'show__theater', 'show__movie')
    search_fields = ('seat_number', 'show__movie__title', 'show__theater__name')
    ordering = ('show', 'seat_number')
    autocomplete_fields = ['show']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'total_price', 'created_at', 'is_cancelled')
    list_filter = ('show__movie', 'show__theater', 'is_cancelled', 'created_at')
    search_fields = ('user__username', 'id', 'show__movie__title', 'show__theater__name', 'is_cancelled')
    date_hierarchy = 'created_at'
    autocomplete_fields = ['user', 'show', 'seats']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('booking__id', 'transaction_id')
    autocomplete_fields = ['booking']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_code', 'booking', 'seat', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('ticket_code', 'booking__id', 'seat__seat_number')
    autocomplete_fields = ['booking', 'seat']
