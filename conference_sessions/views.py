from rest_framework import viewsets
from conference_sessions.models import Session
from conference_sessions.serializers import SessionSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
