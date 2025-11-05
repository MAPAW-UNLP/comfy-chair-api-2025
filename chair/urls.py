from django.urls import path
from .api import (
    CreateReviewAssignmentAPI,
    DeleteReviewAssignmentAPI,
    AvailableReviewersAPI,
    CutoffSelectionAPI,
    ScoreThresholdSelectionAPI,
)

urlpatterns = [
    path('chair/new/', CreateReviewAssignmentAPI.as_view(), name='create-review-assignment'),
    path('chair/<int:reviewer_id>/<int:article_id>/delete/', DeleteReviewAssignmentAPI.as_view(), name='delete-review-assignment'),
    path('chair/articles/<int:article_id>/available-reviewers/', AvailableReviewersAPI.as_view(), name='available-reviewers'),
    path("selection/cut-off/<int:session_id>/", CutoffSelectionAPI.as_view(), name="selection-cut-off"),
    path("selection/score-threshold/<int:session_id>/", ScoreThresholdSelectionAPI.as_view(), name="selection-score-threshold"),
]
