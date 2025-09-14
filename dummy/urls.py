from django.urls import path
from .api import ListDummiesAPI, CreateDummyAPI, DummyAPI, RegistroUsuarioAPI, LoginAPI

urlpatterns = [
    path('', ListDummiesAPI.as_view(), name='list-dummies'),
    path('new/', CreateDummyAPI.as_view(), name='create-dummy'),
    path('test/', DummyAPI.as_view(), name='test-endpoint'),
    path("registro/", RegistroUsuarioAPI.as_view(), name="registro-usuario"),
    path("login/", LoginAPI.as_view(), name="login"),
]
