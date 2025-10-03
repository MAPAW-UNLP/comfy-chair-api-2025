from rest_framework import serializers
from admins.models import Conferencia
from datetime import date

class ConferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conferencia
        fields = '__all__'

    def validate_titulo(self, value):
        # para el caso de guarda la edición se puede repetir el nombre
        conferencia_id = self.instance.id if self.instance else None
        if Conferencia.objects.filter(titulo=value).exclude(id=conferencia_id).exists():
            raise serializers.ValidationError("Ya existe una conferencia con este nombre.")
        return value
    
    def validate(self, data):
        hoy = date.today()
        fecha_ini = data.get('fecha_ini')
        fecha_fin = data.get('fecha_fin')

        # verificacion de que ambas fechas sean a partir de hoy
        if fecha_ini and fecha_ini < hoy:
            raise serializers.ValidationError({"fecha_ini": "La fecha de inicio debe ser hoy o en el futuro."})
        if fecha_fin and fecha_fin < hoy:
            raise serializers.ValidationError({"fecha_fin": "La fecha de fin debe ser hoy o en el futuro."})

        # verificacion que fecha_fin no sea anterior a fecha_ini
        if fecha_ini and fecha_fin and fecha_fin < fecha_ini:
            raise serializers.ValidationError({"fecha_fin": "La fecha de fin no puede ser anterior a la fecha de inicio."})

        return data