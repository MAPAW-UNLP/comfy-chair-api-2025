from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
   
    #Nacho: dejo los roles comentados por el primer sprint porque no los usamos por ahora
    """
    roles = serializers.ListField(
       child=serializers.CharField(),
       allow_empty=True
    )
    """
   
    class Meta:
        model = User
        # Nacho: dejo los roles comentados por el primer sprint porque no los usamos por ahora
        # fields = ['id', 'username', 'first_name', 'last_name', 'affiliation', 'email', 'roles']
        fields = ['id', 'username', 'first_name', 'last_name', 'affiliation', 'email']
