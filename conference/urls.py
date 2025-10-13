from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConferenciaViewSet

router = DefaultRouter()
router.register(r'', ConferenciaViewSet)

urlpatterns = [
    path('', include(router.urls))
]

