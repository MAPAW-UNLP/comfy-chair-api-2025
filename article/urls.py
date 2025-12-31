from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet #, ArticleDeletionRequestViewSet No esta definido

router = DefaultRouter()

router.register(r'article', ArticleViewSet, basename='article')
# router.register(r'article-deletion-request', ArticleDeletionRequestViewSet, basename='article-deletion-request')

urlpatterns = router.urls
