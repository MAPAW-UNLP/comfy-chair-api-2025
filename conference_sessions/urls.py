from rest_framework.routers import DefaultRouter
from .views import ConferenceSessionViewSet

router = DefaultRouter()
router.register(r'conference_sessions', ConferenceSessionViewSet, basename='conference_sessions')

urlpatterns = router.urls
