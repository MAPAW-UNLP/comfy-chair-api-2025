from rest_framework import serializers
from .models import Session
from conference.models import Conference
from conference.serializers import ConferenceSerializer
from user.models import User
from datetime import date

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


    def validate_title(self, value):
        # permite cambiar el título del objeto actual 
        session_id = self.instance.id if self.instance else None
        if Session.objects.filter(title=value).exclude(id=session_id).exists():
            raise serializers.ValidationError("Ya existe una sesión con este nombre.")
        return value

    def validate(self, data):
        # Normalizar lista final de chairs:
        # - si no viene 'chairs' en una edición, usar los chairs actuales de la instancia
        # - si viene explícito (incluso vacío) aplicarlo tal cual
        chairs = data.get('chairs', None)
        if chairs is None and self.instance is not None:
            current_chairs_qs = self.instance.chairs.all()
            if current_chairs_qs.count() == 0:
                raise serializers.ValidationError({"chairs": "Se requiere al menos un chair para la sesión."})
            chairs_final = current_chairs_qs
        else:
            # creación o actualización con 'chairs' explícito
            if not chairs or len(chairs) == 0:
                raise serializers.ValidationError({"chairs": "Se requiere al menos un chair para la sesión."})
            chairs_final = chairs

        # Obtener la conferencia asociada (viene en data o en la instancia)
        conference = data.get('conference') or getattr(self.instance, 'conference', None)
        if conference is None:
            # sin conferencia asociada no se puede validar la regla de exclusión aquí
            return data

        if not isinstance(conference, Conference):
            try:
                conference = Conference.objects.get(pk=conference)
            except Conference.DoesNotExist:
                raise serializers.ValidationError({"conference": "Conferencia no encontrada."})

        # ids de chairs de la conferencia
        conf_chair_ids = set(conference.chairs.values_list('id', flat=True))

        # Normalizar chairs_final a ids para comparar (acepta instancias o pks)
        chairs_ids = []
        for c in chairs_final:
            cid = getattr(c, 'id', None)
            if cid is None:
                try:
                    cid = int(c)
                except Exception:
                    continue
            chairs_ids.append(cid)

        # detectar offending ids (chairs que ya son chairs de la misma conferencia)
        offending = [cid for cid in chairs_ids if cid in conf_chair_ids]
        if offending:
            raise serializers.ValidationError({
                "chairs": "No se puede asignar como chair de sesión a usuarios que ya son chairs de la misma conferencia.",
                "offending_ids": offending
            })

        return data
