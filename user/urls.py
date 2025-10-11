from django.urls import path
from .api import RegistroUsuarioAPI, LoginAPI, GetUsuarioIdAPI, RegistroAdminAPI, GetUsuariosAPI

urlpatterns = [
    path("registro/", RegistroUsuarioAPI.as_view(), name="registro-usuario"),
    path('registro-admin/', RegistroAdminAPI.as_view(), name='registro_admin'),
    path("login/", LoginAPI.as_view(), name="login"),
    path('getUsuario/', GetUsuarioIdAPI.as_view(), name='usuario-actual'),
    path('getUsuarios/', GetUsuariosAPI.as_view(), name='usuarios-lista'), # Creado por el Grupo 1 para traer todos los usuarios de la base de datos
]
