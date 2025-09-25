import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import Usuario
from .serializers import UsuarioSerializer, LoginSerializer

class RegistroUsuarioAPI(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, rol="user")  

class RegistroAdminAPI(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, rol="admin")  


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            payload = {
                "user_id": user.id,
                "rol": user.rol,
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
                    "nombre_completo": user.nombre_completo,
                    "afiliacion": user.afiliacion,
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
            usuario = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        
        return JsonResponse({
            'id': usuario.id,
            'nombre_completo': usuario.nombre_completo,
            'email': usuario.email,
            'afiliacion': usuario.afiliacion,
        }, status=200)