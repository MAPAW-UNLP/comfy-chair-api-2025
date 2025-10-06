from django.urls import path
from . import views
from .api import *

urlpatterns = [ 
    path('new/', CreateAssignmentReviewAPI.as_view(), name='create-assignment-review'),
    path('reviews/<int:reviewer_id>/<int:article_id>/delete/', DeleteAssignmentReviewAPI.as_view(), name='delete-assignment-review'),
    path('articulos/<int:article_id>/revisores-disponibles/', views.get_available_reviewers, name='revisores_disponibles'),
]