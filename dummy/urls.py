from django.urls import path
from .api import DummyAPI

urlpatterns = [
    path('test/', DummyAPI.as_view(), name='test-endpoint'),
]
