from rest_framework import serializers
from .models import Session
from conferences.serializers import ConferenceSerializer
from conferences.models import Conference

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'name' ]

class SessionSerializer(serializers.ModelSerializer):
    conference = ConferenceSerializer(read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'title', 'deadline', 'conference']
