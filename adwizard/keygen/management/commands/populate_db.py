from django.core.management.base import BaseCommand
from keygen.models import Key


class Command(BaseCommand):
    help = '''Create keys in keygen_app.
              Usage: manage.py populate_db'''

    def _create_keys(self):
        key = Key.objects.create_code(size=4)
        key.save()

    def handle(self, *args, **options):
        for _ in range(50):
            self._create_keys()
