import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from theaters.models import Show, Screen
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------------- CHOICES ----------------------

SEAT_TYPE_CHOICES = [
    ('regular', 'Regular'),
    ('vip', 'VIP'),
    ('premium', 'Premium'),
]

BOOKING_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled_user', 'Cancelled by User'),
    ('cancelled_system', 'Cancelled by System'),
    ('expired', 'Expired (Unpaid)'),
    ('refunded', 'Refunded'),
]


PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
]

PAYMENT_METHOD_CHOICES = [
    ('upi', 'UPI'),
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('net_banking', 'Net Banking'),
    ('paytm_wallet', 'Paytm Wallet'),
    ('phonepe', 'PhonePe'),
    ('gpay', 'Google Pay'),
    ('amazon_pay', 'Amazon Pay'),
    ('cash', 'Cash'),
]

# ---------------------- HELPERS ----------------------

def generate_ticket_code():
    return str(uuid.uuid4())[:12].upper()

# ---------------------- MODELS ----------------------

class ShowSeatPricing(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seat_pricing')
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('show', 'seat_type')

    def __str__(self):
        return f"{self.show} - {self.seat_type} - ₹{self.price}"


class Seat(models.Model):
    screen = models.ForeignKey(Screen, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES)

    def get_price(self, show):
        pricing = ShowSeatPricing.objects.filter(show=show, seat_type=self.seat_type).first()
        return pricing.price if pricing else 0

    def __str__(self):
        return f"{self.seat_number} ({self.seat_type}) - {self.screen.theater.name} - {self.screen.name}"



class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username}"


class BookedSeat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='booked_seats')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='booked_seats')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_seats')

    class Meta:
        unique_together = ('show', 'seat')

    def __str__(self):
        return f"Booked {self.seat} for {self.booking}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id} - {self.status}"


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    ticket_code = models.CharField(max_length=12, unique=True, default=generate_ticket_code)
    issued_at = models.DateTimeField(default=now)
    qr_code = models.ImageField(upload_to='tickets/qr_codes/', blank=True, null=True)

    class Meta:
        unique_together = ('booking', 'seat')

    def generate_qr_code(self):
        data = f"Ticket: {self.ticket_code}, Show: {self.show.id}, Seat: {self.seat.seat_number}, Booking ID: {self.booking.id}"
        qr = qrcode.make(data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f"{self.ticket_code}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.show_id:
            self.show = self.booking.show
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.ticket_code} - Seat {self.seat.seat_number}"

# ---------------------- SIGNALS ----------------------

@receiver(post_save, sender=Payment)
def create_tickets_after_payment(sender, instance, created, **kwargs):
    booking = instance.booking
    if instance.status == 'success' and not booking.tickets.exists():
        for seat in booking.seats.all():
            Ticket.objects.create(booking=booking, seat=seat, show=booking.show)
