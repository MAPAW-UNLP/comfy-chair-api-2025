from django.urls import path
from . import views
from .api import *

urlpatterns = [
    path('articulos/<int:articulo_id>/revisores-disponibles/', views.get_revisores_disponibles, name='revisores_disponibles'),    
    path('new/', CreateAssignmentReviewAPI.as_view(), name='create-assignment-review'),
]