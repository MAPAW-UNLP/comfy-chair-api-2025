
from rest_framework import serializers

from dummy.models import Dummy


class DummySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dummy
        fields = ['id', 'name', 'created_at']
