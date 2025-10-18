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
        # para el caso de guarda la edición se puede repetir el nombre
        conferencia_id = self.instance.id if self.instance else None
        if Conference.objects.filter(title=value).exclude(id=conferencia_id).exists():
            raise serializers.ValidationError("Ya existe una conferencia con este nombre.")
        return value
    
    def validate(self, data):
        hoy = date.today()
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # verificacion de que ambas fechas sean a partir de hoy
        if start_date and start_date < hoy:
            raise serializers.ValidationError({"start_date": "La fecha de inicio debe ser hoy o en el futuro."})
        if end_date and end_date < hoy:
            raise serializers.ValidationError({"end_date": "La fecha de fin debe ser hoy o en el futuro."})

        # verificacion que end_date no sea anterior a start_date
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "La fecha de fin no puede ser anterior a la fecha de inicio."})

        return data
