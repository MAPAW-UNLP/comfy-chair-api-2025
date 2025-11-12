from django.contrib import admin
from .models import Article, ArticleDeletionRequest

admin.site.register(Article)
admin.site.register(ArticleDeletionRequest)
