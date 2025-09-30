from django.shortcuts import render
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # Si no hay usuario autenticado, devuelve todos los artículos
        if self.request.user.is_authenticated:
            return self.queryset.filter(authors=self.request.user)
        return self.queryset.all()
