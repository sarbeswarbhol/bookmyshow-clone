from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a default superuser if not exists'

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                phone="9999999999",
                location="Admin City",
                date_of_birth="1990-01-01",
                gender="other",
                role="admin"
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Superuser '{username}' already exists."))
