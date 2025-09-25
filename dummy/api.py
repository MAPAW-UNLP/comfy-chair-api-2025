import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import Dummy, Usuario
from .serializers import DummySerializer, UsuarioSerializer, LoginSerializer

class DummyAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Dummy endpoint working!'})

class CreateDummyAPI(APIView):
    def post(self, request):
        serializer = DummySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

class ListDummiesAPI(APIView):
    def get(self, request):
        dummies = Dummy.objects.all()
        serializer = DummySerializer(dummies, many=True)
        return JsonResponse(serializer.data, safe=False)


class RegistroUsuarioAPI(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            payload = {
                "user_id": user.id,
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