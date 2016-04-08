from rest_framework import serializers
from keygen.models import Key, key_generator


class KeySerializer(serializers.ModelSerializer):

    class Meta:
        model = Key
        fields = ('code', 'created', 'status', 'issued', 'expired',)
        read_only_fields = ('code', 'status', 'issued', 'expired')
