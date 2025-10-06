from django.urls import path
from . import views
from .api import *

urlpatterns = [ 
    path('new/', CreateAssignmentReviewAPI.as_view(), name='create-assignment-review'),
    path('articulos/<int:article_id>/revisores-disponibles/', views.get_available_reviewers, name='revisores_disponibles'),
]