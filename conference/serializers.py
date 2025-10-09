from rest_framework import serializers
from .models import Conference

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'blind_kind']
