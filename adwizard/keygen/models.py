from django.db import models
from django.utils.translation import ugettext_lazy as _
import string
import random


def key_generator(size=4,
                  chars=string.ascii_uppercase +
                  string.ascii_lowercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


class KeyManager(models.Manager):
    def create_code(self, size):
        self.code = key_generator(size=size)
        while Key.objects.filter(code=self.code).exists():
            self.code = key_generator(size=size)
        key = self.create(code=self.code)
        return key


class Key(models.Model):

    STATUS_CHOICES = (
        ('status_free', _('Free to use')),
        ('status_issued', _('Issued')),
        ('status_expired', _('Expired')),
    )

    code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='status_free')
    issued = models.DateTimeField(null=True)
    expired = models.DateTimeField(null=True)

    objects = KeyManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.code
