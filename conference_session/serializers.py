from rest_framework import serializers
from .models import Session
from conference.models import Conference
from conference.serializers import ConferenceSerializer
from user.models import User

class SessionSerializer(serializers.ModelSerializer):

    # Para lectura (anidado)
    conference = ConferenceSerializer(read_only=True)

    # Para escritura (id)
    conference_id = serializers.PrimaryKeyRelatedField(
        queryset=Conference.objects.all(), source='conference', write_only=True
    )

    class Meta:
        model = Session
        fields = '__all__'

    def validate(self, data):
        # exigir al menos un chair en creación
        if self.instance is None:
            chairs = data.get('chairs')
            if not chairs or len(chairs) == 0:
                raise serializers.ValidationError({"chairs": "Se requiere al menos un chair para crear la sesión."})

        # prohibir asignar como chair de sesión a usuarios que ya son chairs de la misma conferencia
        conference = data.get('conference') or getattr(self.instance, 'conference', None)
        if not conference:
            return data  

        # obtener instancia si vienen PK
        if not isinstance(conference, Conference):
            try:
                conference = Conference.objects.get(pk=conference)
            except Conference.DoesNotExist:
                raise serializers.ValidationError({"conference": "Conferencia no encontrada."})

        conf_chair_ids = set(conference.chairs.values_list('id', flat=True))

        chairs = data.get('chairs') or []
        offending = []
        for c in chairs:
            cid = getattr(c, 'id', None)
            if cid is None:
                try:
                    cid = int(c)
                except Exception:
                    continue
            if cid in conf_chair_ids:
                offending.append(cid)

        if offending:
            raise serializers.ValidationError({
                "chairs": "No se puede asignar como chair de sesión a usuarios que ya son chairs de la misma conferencia.",
                "offending_ids": offending
            })

        return data