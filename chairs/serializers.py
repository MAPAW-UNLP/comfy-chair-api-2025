
from rest_framework import serializers

from chairs.models import AssignmentReview


class AssignmentReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentReview
        fields = ['id', 'revisor', 'articulo', 'revisado']