from django.contrib import admin
from .models import Article

# Registramos el modelo para que aparezca en el admin
admin.site.register(Article)
