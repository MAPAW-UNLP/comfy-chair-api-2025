from django.urls import path
from .views import test_endpoint

urlpatterns = [
    path('test/', test_endpoint, name='test-endpoint'),
]
