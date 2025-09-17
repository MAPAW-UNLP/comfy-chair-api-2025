from rest_framework.views import APIView
from rest_framework import generics, status
from django.http import JsonResponse
from .models import Dummy, Usuario
from .serializers import DummySerializer, UsuarioSerializer, LoginSerializer
from rest_framework.response import Response

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
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response({
                "status": "ok",
                "user": {
                    "id": user.id,
                    "nombre_completo": user.nombre_completo,
                    "apellido": user.apellido,
                    "email": user.email,
                }
            })
        return Response(
            {"error": "Email o contraseña incorrecto."},
            status=status.HTTP_401_UNAUTHORIZED
        )