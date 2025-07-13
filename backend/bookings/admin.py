from django.contrib import admin
from .models import Seat, Booking, Payment, Ticket

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'seat_type', 'price', 'show', 'is_booked')
    list_filter = ('seat_type', 'is_booked', 'show')
    search_fields = ('seat_number',)
    ordering = ('show', 'seat_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'total_price', 'created_at')
    list_filter = ('show__movie', 'show__theater')
    search_fields = ('user__username', 'id')
    date_hierarchy = 'created_at'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('booking__id', 'transaction_id')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_code', 'booking', 'seat', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('ticket_code', 'booking__id', 'seat__seat_number')
