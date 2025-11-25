from rest_framework.routers import DefaultRouter
from .views import SessionViewSet
from django.urls import path
from .api import LockSelection

router = DefaultRouter()
router.register(r'session', SessionViewSet, basename='session')

urlpatterns = router.urls + [
    path("session/<int:pk>/lock-selection/", LockSelection.as_view(), name="lock-selection"),
]