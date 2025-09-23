from rest_framework import permissions, viewsets
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-title')  
    serializer_class = ArticleSerializer
    # permissions.IsAuthenticated = solo los usuarios que hayan iniciado sesión pueden usar elendpoint
    permission_classes = [permissions.AllowAny]  # para debbugear voy a usar esto = Cualquiera puede acceder, incluso anónimos
