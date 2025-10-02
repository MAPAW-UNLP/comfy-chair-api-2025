from rest_framework import viewsets
from .models import ConferenceSession
from .serializers import ConferenceSessionSerializer, ConferenceSessionCreateUpdateSerializer

class ConferenceSessionViewSet(viewsets.ModelViewSet):
    queryset = ConferenceSession.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConferenceSessionCreateUpdateSerializer
        return ConferenceSessionSerializer
