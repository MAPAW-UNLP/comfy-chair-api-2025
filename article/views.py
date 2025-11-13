from rest_framework import status
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
from article.models import Article, ArticleDeletionRequest
from .serializers import ArticleSerializer, ArticleDeletionRequestSerializer

# --- Endpoints para el modelo Article ---
class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para el alta de un articulo
    #------------------------------------------------------------
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
    
    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para la modificación de un articulo
    #------------------------------------------------------------
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
    
    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para descargar el archivo principal
    #------------------------------------------------------------
    @action(detail=True, methods=['get'])
    def download_main(self, request, pk=None):
        article = self.get_object()
        if not article.main_file:
            raise Http404("Este artículo no tiene archivo principal.")
        response = FileResponse(article.main_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{article.main_file.name.split("/")[-1]}"'
        return response

    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para descargar el archivo de fuentes
    #------------------------------------------------------------
    @action(detail=True, methods=['get'])
    def download_source(self, request, pk=None):
        article = self.get_object()
        if not article.source_file:
            raise Http404("Este artículo no tiene archivo fuente.")
        response = FileResponse(article.source_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{article.source_file.name.split("/")[-1]}"'
        return response
    
    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para obtener articulos por id de conferencia
    #------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='getArticlesByConferenceId/(?P<conference_id>[^/.]+)')
    def getArticlesByConferenceId(self, request, conference_id=None):
        articles = Article.objects.filter(session__conference_id=conference_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # GRUPO 3 - Endpoint para obtener articulos por id de sesión
    @action(detail=False, methods=['get'], url_path='getArticlesBySessionId/(?P<session_id>[^/.]+)')
    def getArticlesBySessionId(self, request, session_id=None):
        articles = Article.objects.filter(session_id=session_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

# --- Endpoints para el modelo ArticleDeletionRequest ---
class ArticleDeletionRequestViewSet(viewsets.ModelViewSet):
    
    queryset = ArticleDeletionRequest.objects.all()
    serializer_class = ArticleDeletionRequestSerializer

    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para aceptar una solicitud de baja de articulo cuando ya fue aceptado
    #------------------------------------------------------------
    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        deletion_request = self.get_object()
        deletion_request.status = 'accepted'
        deletion_request.save()
        deletion_request.article.delete()
        return Response({'message': 'Solicitud aceptada y artículo eliminado'}, status=status.HTTP_200_OK)

    #------------------------------------------------------------
    # GRUPO 1 - Endpoint para rechazar una solicitud de baja de articulo cuando ya fue aceptado
    #------------------------------------------------------------
    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        deletion_request = self.get_object()
        deletion_request.status = 'rejected'
        deletion_request.save()
        return Response({'message': 'Solicitud rechazada'}, status=status.HTTP_200_OK)
    