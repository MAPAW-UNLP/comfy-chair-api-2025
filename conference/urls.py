from rest_framework.routers import DefaultRouter
from .views import ConferenceViewSet

router = DefaultRouter()
router.register(r'conference', ConferenceViewSet, basename='conference')

urlpatterns = router.urls
