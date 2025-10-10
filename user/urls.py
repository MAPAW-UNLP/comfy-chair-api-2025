from django.urls import path
from .api import RegistroUsuarioAPI, LoginAPI, GetUsuarioIdAPI, RegistroAdminAPI

urlpatterns = [
    path("registro/", RegistroUsuarioAPI.as_view(), name="registro-usuario"),
    path('registro-admin/', RegistroAdminAPI.as_view(), name='registro_admin'),
    path("login/", LoginAPI.as_view(), name="login"),
    path('getUsuario/', GetUsuarioIdAPI.as_view(), name='usuario-actual'),
]