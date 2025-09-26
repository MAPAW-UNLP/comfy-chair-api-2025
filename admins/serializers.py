from rest_framework import serializers
from admins.models import Conferencia

class ConferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conferencia
        fields = '__all__'
