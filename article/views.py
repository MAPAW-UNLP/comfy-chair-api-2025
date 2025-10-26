from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from article.models import Article
from .serializers import ArticleSerializer

from rest_framework.decorators import action

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    serializer_class = ArticleSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors,
                'data_received': request.data
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # endpoint hecho por grupo 3 para obtener articulos en base a la id de una sesion dada
    @action (detail=False, methods=['get'])
    def getArticlesBySessionId (self, request, session_id):
        articles = Article.objects.filter(session_id = session_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)