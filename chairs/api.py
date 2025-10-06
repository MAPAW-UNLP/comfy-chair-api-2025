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
