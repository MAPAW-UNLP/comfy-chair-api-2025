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
        # Normalizar chairs final (si no viene en PATCH usar los existentes)
        chairs = data.get('chairs', None)
        if chairs is None and self.instance is not None:
            current_chairs_qs = self.instance.chairs.all()
            if current_chairs_qs.count() == 0:
                raise serializers.ValidationError({"chairs": "Se requiere al menos un chair para la sesión."})
            chairs_final = current_chairs_qs
        else:
            if not chairs or len(chairs) == 0:
                raise serializers.ValidationError({"chairs": "Se requiere al menos un chair para la sesión."})
            chairs_final = chairs

        # Conference viene ya como instancia por conference_id (source='conference')
        conference = data.get('conference') or getattr(self.instance, 'conference', None)
        if conference is None:
            raise serializers.ValidationError({"conference": "Se requiere una conferencia válida para la sesión."})

        # Si por alguna razón vino como PK, obtener la instancia
        if not isinstance(conference, Conference):
            try:
                conference = Conference.objects.get(pk=conference)
            except Conference.DoesNotExist:
                raise serializers.ValidationError({"conference": "Conferencia no encontrada."})

        # 1) Verificar deadline 
        deadline = data.get('deadline') if 'deadline' in data else getattr(self.instance, 'deadline', None)
        if deadline is None:
            raise serializers.ValidationError({"deadline": "Se requiere un deadline para la sesión."})

        start = conference.start_date
        end = conference.end_date
        if start and end and (deadline < start or deadline > end):
            raise serializers.ValidationError({"deadline": "El deadline debe estar entre las fechas de inicio y fin de la conferencia."})

        # 2) Prohibir chairs que ya son chairs de la misma conferencia
        conf_chair_ids = set(conference.chairs.values_list('id', flat=True))

        chairs_ids = []
        for c in chairs_final:
            cid = getattr(c, 'id', None)
            if cid is None:
                try:
                    cid = int(c)
                except Exception:
                    continue
            chairs_ids.append(cid)

        offending = [cid for cid in chairs_ids if cid in conf_chair_ids]
        if offending:
            raise serializers.ValidationError({
                "chairs": "No se puede asignar como chair de sesión a usuarios que ya son chairs de la misma conferencia.",
                "offending_ids": offending
            })

        return data
