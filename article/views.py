from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from article.models import Article
from .serializers import ArticleSerializer
from django.http import FileResponse, Http404
from rest_framework.decorators import action
from rest_framework import viewsets, status

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
    @action(detail=False, methods=['get'], url_path='getArticlesBySessionId/(?P<session_id>[^/.]+)')
    def getArticlesBySessionId(self, request, session_id=None):
        articles = Article.objects.filter(session_id=session_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors,
                'data_received': request.data
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download_main(self, request, pk=None):
        article = self.get_object()
        if not article.main_file:
            raise Http404("Este artículo no tiene archivo principal.")
        response = FileResponse(article.main_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{article.main_file.name.split("/")[-1]}"'
        return response

    @action(detail=True, methods=['get'])
    def download_source(self, request, pk=None):
        article = self.get_object()
        if not article.source_file:
            raise Http404("Este artículo no tiene archivo fuente.")
        response = FileResponse(article.source_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{article.source_file.name.split("/")[-1]}"'
        return response
    
    @action(detail=True, methods=['delete'])
    def delete_article(self, request, pk=None):
        article = self.get_object()
        article.delete()
        return Response({'message': 'Artículo eliminado correctamente'}, status=status.HTTP_200_OK)
    
