
from django.http import JsonResponse

def test_endpoint(request):
	return JsonResponse({'message': 'Dummy endpoint working!'})
