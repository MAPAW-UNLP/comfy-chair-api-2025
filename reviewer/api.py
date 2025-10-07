from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from reviewer.models import Review, Article, Bid, User
from reviewer.serializers import ReviewerDetailSerializer,ArticleSerializer, BidSerializer, BidUpdateSerializer

# GET /api/articles
class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

# GET /api/articles/{id}
class ArticleDetailView(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

# POST /api/bidding
class BiddingView(APIView):
    def post(self, request):
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# PUT /api/bidding/{id}
class BiddingUpdateView(APIView):
    def put(self, request, id):
        #Busca el bid con el id, si no lo encuentra retorna 404
        bid = get_object_or_404(Bid, id=id)
        serializer = BidUpdateSerializer(bid, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /api/bids?reviewerId=123
class ReviewerBidsView(APIView):
    def get(self, request):
        reviewer_id = request.GET.get('reviewerId')
        if not reviewer_id:
            return Response({"error": "reviewerId parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        #Se omite la verificacion del id, al no tener el modelo de User
        bids = Bid.objects.filter(reviewer_id=reviewer_id)
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

       
# GET /api/reviewers/{id}
class ReviewerDetailView(APIView):
    def get(self,request,id):
        try:
            # Buscar cualquier usuario por ID, ver si agregar verificacion de roles mas adelante..
            reviewer = User.objects.get(id=id)
            serializer = ReviewerDetailSerializer(reviewer)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": f"Usuario con ID {id} no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )

 