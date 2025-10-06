from django.urls import path
from .api import ArticleListView, ArticleDetailView, BiddingView,BiddingUpdateView, ReviewerBidsView, ReviewerDetailView
urlpatterns = [
    path('api/articles', ArticleListView.as_view()),
    path('api/articles/<int:pk>', ArticleDetailView.as_view()),
    path('api/bidding', BiddingView.as_view()),
    path('bidding/<int:id>/', BiddingUpdateView.as_view(), name='bidding-update'),
    path('bidding/', ReviewerBidsView.as_view(), name='reviewer-bids'),
    path('api/reviewers/<int:id>/', ReviewerDetailView.as_view(), name='reviewer-detail'),
]
