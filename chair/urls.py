from django.urls import path
from .api import (
    CreateReviewAssignmentAPI,
    DeleteReviewAssignmentAPI,
    AvailableReviewersAPI,
    CutoffSelectionAPI,
)

urlpatterns = [
    path('chair/new/', CreateReviewAssignmentAPI.as_view(), name='create-review-assignment'),
    path('chair/<int:reviewer_id>/<int:article_id>/delete/', DeleteReviewAssignmentAPI.as_view(), name='delete-review-assignment'),
    path('chair/articles/<int:article_id>/available-reviewers/', AvailableReviewersAPI.as_view(), name='available-reviewers'),
    path("selection/fixed/<int:session_id>/", CutoffSelectionAPI.as_view(), name="selection-fixed"),
]
