from django.urls import path
from .api import ArticleListView, ArticleDetailView, BiddingView

urlpatterns = [
    path('api/articles', ArticleListView.as_view()),
    path('api/articles/<int:pk>', ArticleDetailView.as_view()),
    path('api/bidding', BiddingView.as_view()),
]
