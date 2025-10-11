from rest_framework import viewsets
from conference.models import Conference
from conference.serializers import ConferenceSerializer

class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer