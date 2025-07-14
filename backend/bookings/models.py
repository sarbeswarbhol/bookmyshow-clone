import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from theaters.models import Show
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

SEAT_TYPE_CHOICES = [
    ('regular', 'Regular'),
    ('vip', 'VIP'),
    ('premium', 'Premium'),
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

def generate_ticket_code():
    return str(uuid.uuid4())[:12].upper()


class ShowSeatPricing(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seat_pricing')
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('show', 'seat_type')

    def __str__(self):
        return f"{self.show} - {self.seat_type} - ₹{self.price}"


class Seat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)  # e.g., A1, B3
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES, default='regular')
    is_booked = models.BooleanField(default=False)

    def get_price(self):
        pricing = ShowSeatPricing.objects.filter(show=self.show, seat_type=self.seat_type).first()
        if pricing:
            return pricing.price
        return 0 


    def __str__(self):
        return f"{self.seat_number} ({self.seat_type}) - {self.show}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f"Booking #{self.id} by {self.user.username}"


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
    ticket_code = models.CharField(max_length=12, unique=True, default=generate_ticket_code)
    issued_at = models.DateTimeField(default=now)
    qr_code = models.ImageField(upload_to='tickets/qr_codes/', blank=True, null=True)

    def generate_qr_code(self):
        data = f"Ticket: {self.ticket_code}, Seat: {self.seat.seat_number}, Booking ID: {self.booking.id}"
        qr = qrcode.make(data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f"{self.ticket_code}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.ticket_code} - Seat {self.seat.seat_number}"


@receiver(post_save, sender=Booking)
def create_tickets_for_booking(sender, instance, created, **kwargs):
    if created:
        for seat in instance.seats.all():
            Ticket.objects.create(booking=instance, seat=seat)
