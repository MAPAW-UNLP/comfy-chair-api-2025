from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from articles.models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    # print(queryset)
    '''
    Nacho: tuve que comentar lo de arriba porque no ejecutaba las migraciones. 
    Segun ChatGPT: Esa línea se ejecuta en el momento en que Django importa el archivo, 
    no cuando se hace una petición. Y como en ese momento las migraciones todavía no se corrieron 
    (o incluso Django las está preparando), intentar acceder a Article.objects.all() provoca el error:
    '''
    
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