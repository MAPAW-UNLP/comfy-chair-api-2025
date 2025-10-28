from rest_framework import serializers
from .models import Conference
from datetime import date

class ConferenceSerializerGrupo1(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'blind_kind']

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = '__all__'

    def validate_title(self, value):
        # elimina espacios al inicio y final
        value = value.strip()

        # si es editacion, obtener el ID actual
        conferencia_id = self.instance.id if self.instance else None

        # buscar duplicados sin distinguir mayúsculas/minúsculas
        if Conference.objects.filter(title__iexact=value).exclude(id=conferencia_id).exists():
            raise serializers.ValidationError(
                "Ya existe una conferencia con ese título."
            )

        return value

    def validate(self, data):
        # normalizar lista final de chairs
        chairs = data.get('chairs', None)
        if chairs is None and self.instance is not None:
            # usar los chairs actuales
            if self.instance.chairs.count() == 0:
                raise serializers.ValidationError({
                    "chairs": "Se requiere al menos un chair para crear/editar la conferencia."
                })
        else:
            # creación o edición con 'chairs' explícito
            if not chairs or len(chairs) == 0:
                raise serializers.ValidationError({
                    "chairs": "Se requiere al menos un chair para crear/editar la conferencia."
                })

        # Validación de fechas
        hoy = date.today()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # verificacion de que ambas fechas sean a partir de hoy
        if start_date and start_date < hoy:
            raise serializers.ValidationError({
                "start_date": "La fecha de inicio debe ser hoy o en el futuro."
            })
        if end_date and end_date < hoy:
            raise serializers.ValidationError({
                "end_date": "La fecha de fin debe ser hoy o en el futuro."
            })
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "La fecha de fin no puede ser anterior a la fecha de inicio."
            })

        return data
