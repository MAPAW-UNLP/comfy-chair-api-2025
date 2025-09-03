from django.urls import path
from .api import ListDummiesAPI, CreateDummyAPI, DummyAPI

urlpatterns = [
    path('', ListDummiesAPI.as_view(), name='list-dummies'),
    path('new/', CreateDummyAPI.as_view(), name='create-dummy'),
    path('test/', DummyAPI.as_view(), name='test-endpoint'),
]
