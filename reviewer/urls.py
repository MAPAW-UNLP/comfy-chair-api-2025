from django.urls import path
# from .api import ArticleDetailView, ArticleListView
from .api import BiddingUpdateView, BiddingView, ReviewUpdateView, ReviewerBidsView, ReviewerDetailView,ReviewView,ReviewDetailView,ReviewerReviewsView,AssignmentReviewCreateView, ReviewsArticleView
urlpatterns = [
    # path('articles/', ArticleListView.as_view()),
    # path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('bidding/', BiddingView.as_view()),
    path('bidding/<int:id>/', BiddingUpdateView.as_view(), name='bidding-update'),
    path('bids/', ReviewerBidsView.as_view(), name='reviewer-bids'),
    path('reviewers/<int:id>/', ReviewerDetailView.as_view(), name='reviewer-detail'),
    path('reviewers/<int:id>/review/', ReviewerReviewsView.as_view(),name="reviewer-review"),
    path('reviews/',ReviewView.as_view(),name="create-review"),
    path('reviews/<int:articleId>/',ReviewDetailView.as_view(),name="review-detail"),
    path('reviews/assignments/',AssignmentReviewCreateView.as_view(), name="assign-article"),
    path('reviews/<int:id>',ReviewUpdateView.as_view(),name="review-update"),
    path('reviews/article',ReviewsArticleView.as_view(),name="reviews-article")
]