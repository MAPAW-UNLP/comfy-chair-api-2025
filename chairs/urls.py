from django.urls import path
from . import views

urlpatterns = [
    path('articulos/<int:articulo_id>/revisores-disponibles/', views.get_available_reviewers, name='revisores_disponibles'),
]