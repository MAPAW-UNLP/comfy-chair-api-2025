from django.urls import path
# from .api import ArticleDetailView, ArticleListView
from .api import BiddingUpdateView, BiddingView, ReviewUpdateView, ReviewerBidsView, ReviewerDetailView, ReviewsArticleView  
urlpatterns = [
    # path('articles/', ArticleListView.as_view()),
    # path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('bidding/', BiddingView.as_view()),
    path('bidding/<int:id>/', BiddingUpdateView.as_view(), name='bidding-update'),
    path('bids/', ReviewerBidsView.as_view(), name='reviewer-bids'),
    path('reviewers/<int:id>/', ReviewerDetailView.as_view(), name='reviewer-detail'),
    path('reviews/<int:id>/', ReviewUpdateView.as_view()),
    path('reviews/', ReviewsArticleView.as_view())
]
