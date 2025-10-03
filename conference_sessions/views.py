from rest_framework import viewsets
from conference_sessions.models import Session
from conference_sessions.serializers import SessionSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    # Optional: Filtra las sesiones por ID de conferencia
    def get_queryset(self):
        queryset = super().get_queryset()
        conference_id = self.request.query_params.get('conference_id')
        if conference_id:
            queryset = queryset.filter(conference_id=conference_id)
        return queryset