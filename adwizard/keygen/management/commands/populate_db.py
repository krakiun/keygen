from django.core.management.base import BaseCommand
from django.conf import settings
from keygen.models import Key


class Command(BaseCommand):
    help = '''Create keys in keygen_app.
              Usage: manage.py populate_db'''

    def _create_keys(self):
        key = Key.objects.create_code(size=settings.TOKEN_SIZE)
        key.save()

    def handle(self, *args, **options):
        for _ in range(settings.KEYS_QTY):
            self._create_keys()
        print('Created {} keys of size {} symbols in database'.format(settings.KEYS_QTY, settings.TOKEN_SIZE))
