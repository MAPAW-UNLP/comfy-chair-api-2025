from django.urls import path
from .api import AdminRegisterAPI, GetUserIdAPI, GetUserListAPI, LoginAPI, UserRegisterAPI

urlpatterns = [
    path("register/", UserRegisterAPI.as_view(), name="register-user"),
    path('register-admin/', AdminRegisterAPI.as_view(), name='register-admin'),
    path("login/", LoginAPI.as_view(), name="login"),
    path('getUser/', GetUserIdAPI.as_view(), name='user-current'),
    path('getUsers/', GetUserListAPI.as_view(), name='users-list'), # Creado por el Grupo 1 para traer todos los usuarios de la base de datos
]
