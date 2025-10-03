from rest_framework import viewsets
from conferences.models import Conference
from conferences.serializers import ConferenceSerializer

class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer