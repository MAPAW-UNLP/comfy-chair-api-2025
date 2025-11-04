import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer, LoginSerializer

class UserRegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, role="user")  

class AdminRegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

class GetUserIdAPI(APIView):
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
    
# Creado por el Grupo 1 para traer todos los usuarios de la base de datos
# Se requiere para poder seleccionar los autores de un articulo
# No esta protegido por JWT pero deberia estarlo de alguna forma, se deja asi para facilitar el merge
class GetUserListAPI(APIView):
    def get(self, request):
        usuarios = User.objects.all()
        usuarios_data = [
            {
                'id': usuario.id,
                'full_name': usuario.full_name,
                'email': usuario.email,
            } for usuario in usuarios
        ]
        return JsonResponse(usuarios_data, safe=False, status=200)
    
# Lo agregamos desde el grupo 3 para obtener usuarios que sean solo user, se ordena alfabeticamente
# Por ahora se evita usar JWT, se agrega mas adelante
class GetUsersNoAdminAPI(APIView):
    def get(self, request):
        users = User.objects.filter(role="user").order_by('full_name')
        users_data = [
            {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
            } for user in users
        ]
        return JsonResponse(users_data, safe=False, status=200)

# Lo agregamos desde el grupo 3 para obtener usuarios por id
# Por ahora se evita usar JWT, se agrega mas adelante
class GetUserByIdAPI(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user_data = {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
            }
            return JsonResponse(user_data, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)