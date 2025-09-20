from django.urls import path
from . import views

urlpatterns = [
    path('articulos/<int:articulo_id>/revisores-disponibles/', views.get_revisores_disponibles, name='revisores_disponibles'),
]