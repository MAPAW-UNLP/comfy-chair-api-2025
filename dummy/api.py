from rest_framework.views import APIView

from django.http import JsonResponse

class DummyAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Dummy endpoint working!'})
