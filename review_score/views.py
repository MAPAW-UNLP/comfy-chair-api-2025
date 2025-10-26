from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ReviewScore
from .serializers import ReviewScoreSerializer

@api_view(['POST'])
def create_review_score(request):
    """
    Crea un nuevo ReviewScore y devuelve el detalle completo.
    Ejemplo JSON de entrada:
    {
        "user_id": 1,
        "article_id": 5,
        "score": 8.5
    }
    """
    serializer = ReviewScoreSerializer(data=request.data)
    if serializer.is_valid():
        review_score = serializer.save()
        # Re-serializar para incluir los datos anidados del artículo y usuario
        full_serializer = ReviewScoreSerializer(review_score)
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_review_score(request):
    review_scores = ReviewScore.objects.all()
    serializer = ReviewScoreSerializer(review_scores, many=True)
    return Response(serializer.data)
