from rest_framework import serializers
from .models import Session
from conference.models import Conference
from conference.serializers import ConferenceSerializer

class SessionSerializer(serializers.ModelSerializer):
    # Para lectura (anidado)
    conference = ConferenceSerializer(read_only=True)

    # Para escritura (id)
    conference_id = serializers.PrimaryKeyRelatedField(
        queryset=Conference.objects.all(), source='conference', write_only=True
    )

    class Meta:
        model = Session
        fields = ['id', 'title', 'deadline', 'capacity', 'conference', 'conference_id']

