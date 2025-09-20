
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from dummy.models import Dummy
from django.contrib.auth.hashers import make_password
from .models import Usuario
from django.contrib.auth import authenticate


class DummySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dummy
        fields = ['id', 'name', 'created_at']

class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Usuario.objects.all(), message="Email ya registrado.")]
    )

    class Meta:
        model = Usuario
        fields = ["id", "nombre_completo", "apellido", "afiliacion", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # encripta la contraseña
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError({"error": "Email o contraseña incorrecto."})

        data["user"] = user
        return data
