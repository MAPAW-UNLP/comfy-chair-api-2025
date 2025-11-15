from django.urls import path
# from .api import ArticleDetailView, ArticleListView
from .api import BiddingUpdateView, BiddingView, ReviewPublishView, ReviewUpdateDraftView, ReviewUpdatePublishedView, ReviewerBidsView, ReviewerDetailView, ReviewView, ReviewDetailView, ReviewsArticleView, ReviewByReviewerView
urlpatterns = [
    # path('articles/', ArticleListView.as_view()),
    # path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('bidding/', BiddingView.as_view()),
    path('bidding/<int:id>/', BiddingUpdateView.as_view(), name='bidding-update'),
    path('bids/', ReviewerBidsView.as_view(), name='reviewer-bids'),
    path('reviewers/<int:id>/', ReviewerDetailView.as_view(), name='reviewer-detail'),
    path('reviews/',ReviewView.as_view(),name="create-review"),
    path('reviews/<int:articleId>/',ReviewDetailView.as_view(),name="review-detail"),
    path('reviews/<int:id>/updateDraft/',ReviewUpdateDraftView.as_view(),name="review-update-draft"),
    path('reviews/<int:id>/updatePublished/',ReviewUpdatePublishedView.as_view(),name="review-update-published"),
    path('reviews/<int:id>/publish/', ReviewPublishView.as_view(), name='review-publish'),
    path('article/<int:article_id>/reviews/',ReviewsArticleView.as_view(),name="reviews-article"),
    path('reviews/<int:articleId>/<int:reviewerId>/', ReviewByReviewerView.as_view(), name='review-by-reviewer')

]