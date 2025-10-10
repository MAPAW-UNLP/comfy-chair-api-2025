from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate


class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email ya registrado.")]
    )
  

    class Meta:
        model = User
        fields = ["id", "full_name", "affiliation", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data, role=None):
        validated_data["password"] = make_password(validated_data["password"])
        if role:
            validated_data["role"] = role  # Asigna el rol según el endpoint
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
