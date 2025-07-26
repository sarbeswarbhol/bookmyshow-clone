import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import deserialize
from django.db import transaction


class Command(BaseCommand):
    help = "Restore database from a JSON backup file"

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help="Path to the backup JSON file")

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']

        if not os.path.exists(filepath):
            raise CommandError(f"❌ File not found: {filepath}")

        confirm = input(f"⚠ This will overwrite existing data. Are you sure you want to continue? [yes/no]: ")
        if confirm.strip().lower() != 'yes':
            self.stdout.write(self.style.WARNING("❌ Restore cancelled."))
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.stdout.write(self.style.WARNING("⏳ Restoring data..."))

            with transaction.atomic():
                for obj in deserialize('json', json.dumps(data)):
                    obj.save()

            self.stdout.write(self.style.SUCCESS("🎉 Database restore successful."))

        except Exception as e:
            raise CommandError(f"❌ Failed to restore data: {e}")
