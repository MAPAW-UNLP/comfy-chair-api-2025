#from datetime import timezone
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from reviewer.models import Review, Article, Bid, ReviewVersion, User
from chair.models import ReviewAssignment
from reviewer.serializers import ReviewUpdateSerializer, ReviewerDetailSerializer, BidSerializer, BidUpdateSerializer,ReviewSerializer,ReviewVersionSerializer

# # GET /api/articles
# class ArticleListView(APIView):
#     def get(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

# # GET /api/articles/{id}
# class ArticleDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Article.objects.get(pk=pk)
#         except Article.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

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

#POST /api/reviews/
#Guarda una nueva revisión en borrador
class ReviewView(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():   
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#GET /api/review/{articleId}/
#Devuelve la revisión publicado o en borrador de un artículo
class ReviewDetailView(APIView):
    def get(self, request, articleId):
        review = Review.objects.filter(article=articleId).first()
        serializer = ReviewSerializer(review)
        if not review:
            return Response(
               {"message":"No existe una revision de ese articulo"},
               status = status.HTTP_404_NOT_FOUND
           )
        return Response(serializer.data,status=status.HTTP_200_OK)


# GET /api/reviews/reviewer/{reviewerId}/
#Devuelve todas las revisiones publicadas de un revisor
class ReviewsByReviewerIdView(APIView):
    def get(self, request, reviewerId):
        reviews = Review.objects.filter(reviewer_id=reviewerId, is_published=True)
        if not reviews.exists():
            return Response(
                {"message": "No se encontraron revisiones para este revisor"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
# GET /api/reviews/{idReview}/versions/
#Devuelve todas las versiones de una revisión
class ReviewVersionsView(APIView):
    def get(self, request, idReview):
        review = get_object_or_404(Review, id=idReview)
        versions = ReviewVersion.objects.filter(review=review).order_by('version_number')
        if not versions.exists():
            return Response(
                {"message": "No hay versiones disponibles para esta revisión"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewVersionSerializer(versions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#PUT /api/reviews/{idReview}/publish/
class ReviewPublishView(APIView):
      def put(self, request, id):
        review = get_object_or_404(Review, id=id)
        # se necesita modificar el middleware del login, user como objeto no solo el id.      
        # Verificar que el usuario que modifica el estado es el autor
        #if review.review_assignment.reviewer != request.user:
          #  return Response(
         #       {"error": "No tienes permisos para publicar esta revisión"},
        #        status=status.HTTP_403_FORBIDDEN
        #    )        
        # Validaciones
        if review.is_published:
            return Response(
                {"error": "La revisión ya está publicada"},
                status=status.HTTP_400_BAD_REQUEST
            )       
        if review.score is None:
            return Response(
                {"error": "La revisión debe tener una puntuación"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not review.opinion:
            return Response(
                {"error": "La revisión debe tener una opinión"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Usar transacción atómica para garantizar consistencia
        with transaction.atomic():
            try:
                assignment = ReviewAssignment.objects.get(
                    reviewer=review.reviewer,                    
                    article=review.article
                )
                assignment.reviewed = True
                assignment.save()
            except ReviewAssignment.DoesNotExist:
                return Response(
                    {"error": "No se encontró la asignación de revisión"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Publicar la revisión
            review.is_published = True
            review.created_at = timezone.now()  
            review.save()
           #Creo la primera version 
            ReviewVersion.objects.create(
                review=review,
                version_number=1,
                score=review.score,
                opinion=review.opinion,           
                )
        
     
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
      


# PUT api/reviews/{idReview}/updateDraft/
class ReviewUpdateDraftView(APIView):
    def put(self, request, id):
        review = get_object_or_404(Review, id=id)
        # se necesita modificar el middleware del login, user como objeto no solo el id.
        #if review.review_assignment.reviewer != request.user:
        #  return Response({"error": "Sin permisos"}, status=403)
        
        if review.is_published:
            return Response({"error": "Usa el endpoint para revisiones publicadas"}, status=400)
        
        serializer = ReviewUpdateSerializer(review, data=request.data, partial=True)
        # Actualización sin versiones
        if serializer.is_valid():
            updated_review = serializer.save() 
            return Response(ReviewSerializer(updated_review).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUT api/reviews/{idReview}/updatePublished/
class ReviewUpdatePublishedView(APIView):
    def put(self, request, id):
        review = get_object_or_404(Review, id=id)
        # se necesita modificar el middleware del login, user como objeto no solo el id.
        #if review.review_assignment.reviewer != request.user:
         #   return Response({"error": "Sin permisos"}, status=403)
        
        if not review.is_published:
            return Response({"error": "Usa el endpoint para borradores"}, status=400)
        
        serializer = ReviewUpdateSerializer(review, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        try:
            # Actualiza la revision
            updated_review = serializer.save()
            
            # Creo la version con los nuevos valores:
            last_version = review.versions.last()
            new_version_number = last_version.version_number + 1 if last_version else 1
            
            ReviewVersion.objects.create(
                review=updated_review,
                version_number=new_version_number,
                score=updated_review.score,        
                opinion=updated_review.opinion,
            )
            
            return Response(ReviewSerializer(updated_review).data, status=200)
            
        except Exception as e:
            return Response(
                {"error": f"Error al actualizar: {str(e)}"},
                status=500
            )

 
#GET /api/article/<int:article_id>/reviews/    
class ReviewsArticleView(APIView):
   def get(self, request, article_id):  
        # SOLO revisiones publicadas
        reviews = Review.objects.filter(article=article_id, is_published=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response({
            "article_id": article_id,
            "count": reviews.count(),
            "reviews": serializer.data
        })
   
# GET /api/reviews/{articleId}/{reviewerId}/
class ReviewByReviewerView(APIView):
    def get(self, request, articleId, reviewerId):
       review = Review.objects.filter(article_id=articleId, reviewer_id=reviewerId).first()
       if not review:
            return Response({"message": "No existe una revisión de ese artículo para este revisor"}, status=status.HTTP_404_NOT_FOUND)
       serializer = ReviewSerializer(review)
       return Response(serializer.data, status=status.HTTP_200_OK)
