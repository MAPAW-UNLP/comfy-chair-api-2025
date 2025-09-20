from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

# Crea un router y registra nuestra vista de artículos con él.
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

# Las URL generadas por el router se incluyen en el urlpatterns.
urlpatterns = [
    path('', include(router.urls)),
]