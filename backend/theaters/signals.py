from django.db.models.signals import post_save
from django.dispatch import receiver
from bookings.models import ShowSeatPricing, Seat, SEAT_TYPE_CHOICES
from .models import Show

@receiver(post_save, sender=Show)
def setup_show_seating_and_pricing(sender, instance, created, **kwargs):
    if not created:
        return

    seat_map = {
        'vip': ('A', 10, 350),
        'regular': ('B', 15, 200),
        'premium': ('C', 5, 500),
    }

    for seat_type, (row_prefix, count, price) in seat_map.items():
        # Create pricing
        ShowSeatPricing.objects.create(
            show=instance,
            seat_type=seat_type,
            price=price
        )

        # Create seats
        for i in range(1, count + 1):
            seat_number = f"{row_prefix}{i}"
            Seat.objects.create(
                show=instance,
                seat_number=seat_number,
                seat_type=seat_type
            )
