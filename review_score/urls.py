from django.urls import path
from .views import create_review_score, list_review_score

urlpatterns = [
    path('create/score', create_review_score, name='create_review_score'),
    path('list/score', list_review_score, name='list_review_score'),
]
