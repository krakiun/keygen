from django.db import models
from django.utils.translation import ugettext_lazy as _
import string
import random


def key_generator(size=4, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


class KeyManager(models.Manager):
    def create_code(self, size):
        self.code=key_generator(size=size)
        while Key.objects.filter(code=self.code).exists():
            self.code=key_generator(size=size)
        key = self.create(code=self.code)
        return key


class Key(models.Model):

    STATUS_FREE = 1
    STATUS_ISSUED = 2
    STATUS_EXPIRED = 3

    STATUS_CHOICES = (
        (STATUS_FREE, _('Free to use')),
        (STATUS_ISSUED, _('Issued')),
        (STATUS_EXPIRED, _('Expired')),
    )

    code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_FREE)
    issued = models.DateTimeField(null=True)
    expired = models.DateTimeField(null=True)

    objects = KeyManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.code
