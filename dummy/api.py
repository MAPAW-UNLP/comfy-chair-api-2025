from rest_framework.views import APIView

from django.http import JsonResponse
from dummy.models import Dummy
from dummy.serializers import DummySerializer

class DummyAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Dummy endpoint working!'})

class CreateDummyAPI(APIView):
    def post(self, request):
        serializer = DummySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class ListDummiesAPI(APIView):
    def get(self, request):
        dummies = Dummy.objects.all()
        serializer = DummySerializer(dummies, many=True)
        return JsonResponse(serializer.data, safe=False)