import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User
from .serializers import UsuarioSerializer, LoginSerializer

class RegistroUsuarioAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, role="user")  

class RegistroAdminAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, role="admin")  


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            payload = {
                "user_id": user.id,
                "rol": user.role,
                "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            return JsonResponse({
                "status": "ok",
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "affiliation": user.affiliation,
                } 
            }, status=200)

        return JsonResponse(
            {"error": "Email o contraseña incorrecto."},
            status=401
        )

class GetUsuarioIdAPI(APIView):
    def get(self, request):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        
        return JsonResponse({
            'id': usuario.id,
            'full_name': usuario.full_name,
            'email': usuario.email,
            'affiliation': usuario.affiliation,
        }, status=200)