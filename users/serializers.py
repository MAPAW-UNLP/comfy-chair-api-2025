from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'affiliation', 'email', 'roles']
