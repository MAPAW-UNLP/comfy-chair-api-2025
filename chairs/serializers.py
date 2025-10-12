from rest_framework import serializers
from chairs.models import ReviewAssignment


class ReviewAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAssignment
        fields = ['id', 'reviewer', 'article', 'reviewed']
