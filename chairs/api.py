from rest_framework.views import APIView

from django.http import JsonResponse
from chairs.models import AssignmentReview
from chairs.serializers import AssignmentReviewSerializer

class ChairsAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Chairs endpoint working!'})

class CreateAssignmentReviewAPI(APIView):
    def post(self, request):
        serializer = AssignmentReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

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
