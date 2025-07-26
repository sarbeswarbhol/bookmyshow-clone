import json
import os
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.apps import apps
from datetime import datetime


class Command(BaseCommand):
    help = "Backup all data to a JSON file using UTF-8 encoding"

    def handle(self, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"db_backup_{timestamp}.json"

        all_models = apps.get_models()
        all_data = []

        for model in all_models:
            try:
                data = serialize('json', model.objects.all())
                all_data += json.loads(data)
                self.stdout.write(self.style.SUCCESS(f"✔ Serialized {model.__name__}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠ Skipped {model.__name__}: {e}"))

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Backup completed: {output_file}"))
