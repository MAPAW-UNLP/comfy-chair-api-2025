from rest_framework import serializers
from .models import Session
from conferences.serializers import ConferenceSerializer
from conferences.models import Conference

class SessionSerializer(serializers.ModelSerializer):
    conference = serializers.PrimaryKeyRelatedField(queryset=Conference.objects.all())

    class Meta:
        model = Session
        fields = ['id', 'title', 'deadline', 'conference']
