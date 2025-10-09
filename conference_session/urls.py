from rest_framework.routers import DefaultRouter
from .views import SessionViewSet

router = DefaultRouter()
router.register(r'sessions', SessionViewSet, basename='session')

urlpatterns = router.urls