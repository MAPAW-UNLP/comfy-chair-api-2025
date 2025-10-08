from rest_framework.views import APIView

from django.http import JsonResponse
from chairs.models import AssignmentReview
from chairs.serializers import AssignmentReviewSerializer

class ChairsAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Chairs endpoint working!'})

class CreateAssignmentReviewAPI(APIView):
    def post(self, request):
        reviewer_id = request.data.get("reviewer")
        article_id = request.data.get("article")

        if not reviewer_id or not article_id:
            return JsonResponse(
                {"error": "Reviewer y Article son requeridos."}, status=400
            )

        assignment, created = AssignmentReview.objects.update_or_create(
            reviewer_id=reviewer_id,
            article_id=article_id,
            defaults={"is_active": True},
        )

        serializer = AssignmentReviewSerializer(assignment)
        return JsonResponse(serializer.data, status=201 if created else 200)


class DeleteAssignmentReviewAPI(APIView):
    def delete(self, request, *args, **kwargs):
        reviewer_id = kwargs.get('reviewer_id')
        article_id = kwargs.get('article_id')

        if not reviewer_id or not article_id:
            return JsonResponse({'error': 'Missing reviewer_id or article_id'}, status=400)

        try:
            review = AssignmentReview.objects.get(
                reviewer_id=reviewer_id,
                article_id=article_id,
                is_active=True
            )
        except AssignmentReview.DoesNotExist:
            return JsonResponse({'error': 'Reviewer not assigned or already inactive'}, status=404)

        review.is_active = False
        review.save()
        return JsonResponse({'message': 'Reviewer assignment logically deleted'}, status=200)
