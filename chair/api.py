from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from chair.models import ReviewAssignment 
from conference_session.models import Session
from reviewer.models import Bid, Review
from chair.serializers import ReviewAssignmentSerializer
from article.models import Article
from user.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count

class ChairAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Chair endpoint working!'})


class CreateReviewAssignmentAPI(APIView):
    def post(self, request):
        reviewer_id = request.data.get("reviewer")
        article_id = request.data.get("article")

        if not reviewer_id or not article_id:
            # Mensaje en español, pero estructura en inglés
            return JsonResponse(
                {"error": "Reviewer y Article son requeridos."}, status=400
            )

        assignment, created = ReviewAssignment.objects.update_or_create(
            reviewer_id=reviewer_id,
            article_id=article_id,
            defaults={"deleted": False},
        )

        serializer = ReviewAssignmentSerializer(assignment)
        return JsonResponse(serializer.data, status=201 if created else 200)


class DeleteReviewAssignmentAPI(APIView):
    def delete(self, request, *args, **kwargs):
        reviewer_id = kwargs.get('reviewer_id')
        article_id = kwargs.get('article_id')

        if not reviewer_id or not article_id:
            return JsonResponse({'error': 'Missing reviewer_id or article_id'}, status=400)

        try:
            review = ReviewAssignment.objects.get(
                reviewer_id=reviewer_id,
                article_id=article_id,
                deleted=False
            )
        except ReviewAssignment.DoesNotExist:
            return JsonResponse({'error': 'Reviewer not assigned or already inactive'}, status=404)

        review.deleted = True
        review.save()
        return JsonResponse({'message': 'Reviewer assignment logically deleted'}, status=200)


class AvailableReviewersAPI(APIView):
    """
    Devuelve todos los revisores disponibles y asignados, priorizados según el interés.
    """

    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)

        bids = Bid.objects.filter(article=article).select_related('reviewer')

        interested = []
        maybe = []
        not_interested = []
        reviewers_with_bid_ids = []

        for bid in bids:
            reviewers_with_bid_ids.append(bid.reviewer.id)
            reviewer_data = {
                'id': bid.reviewer.id,
                'full_name': bid.reviewer.full_name,
                'email': bid.reviewer.email,
                'interest': bid.interest,
                'assigned': ReviewAssignment.objects.filter(
                    article=article,
                    reviewer=bid.reviewer,
                    deleted=False
                ).exists(),
            }
            if bid.interest == 'interested':
                interested.append(reviewer_data)
            elif bid.interest == 'maybe':
                maybe.append(reviewer_data)
            elif bid.interest == 'not_interested':
                not_interested.append(reviewer_data)

        reviewers_without_bid = User.objects.filter(role = "user").exclude(id__in=reviewers_with_bid_ids)
        none_interest = [
            {
                'id': reviewer.id,
                'full_name': reviewer.full_name,
                'email': reviewer.email,
                'interest': 'none',
                'assigned': ReviewAssignment.objects.filter(
                    article=article,
                    reviewer=reviewer,
                    deleted=False
                ).exists(),
            }
            for reviewer in reviewers_without_bid
        ]

        final_reviewer_list = []
        final_reviewer_list.extend(interested)
        final_reviewer_list.extend(maybe)
        final_reviewer_list.extend(none_interest)
        final_reviewer_list.extend(not_interested)

        # Ordena los revisores priorizando los no asignados
        final_reviewer_list = sorted(final_reviewer_list, key=lambda r: not r['assigned'])

        return JsonResponse(final_reviewer_list, safe=False)
    
    
class CutoffSelectionAPI(APIView):
    def post(self, request, session_id):
        percentage = request.data.get("percentage", 100)
        # Validación de porcentaje
        try:
            percentage = float(percentage)
            if percentage <= 0 or percentage > 100:
                return JsonResponse(
                    {"error": "El porcentaje debe estar entre 0 y 100."},
                    status=400
                )
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "El porcentaje debe ser un número válido."},
                status=400
            )

        # Busca la sesion
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'error': 'Sesión no encontrada'}, status=404)

        # Verifica capacidad de la sesion
        if not session.capacity or session.capacity <= 0:
            return JsonResponse(
                {"error": "La sesión no tiene definida una capacidad válida."},
                status=400
            )

        # Busca articulos en la sesion
        if not Article.objects.filter(session=session).exists():
            return JsonResponse(
                {'message': 'La sesión no tiene artículos asociados.'},
                status=400
            )
        articles = (
            Article.objects.filter(session=session)
            .annotate(avg_score=Avg("review__score"))
            .exclude(avg_score=None)
            .order_by("-avg_score")
        )
        if not articles.exists():
            return JsonResponse(
                {'message': 'No hay artículos con puntajes disponibles para esta sesión.'},
                status=200
            )

        total_articles = articles.count()

        cutoff_index = min(int((percentage / 100) * total_articles), total_articles)
        
        accepted_articles = articles[:cutoff_index]
        rejected_articles = articles[cutoff_index:]
        
        Article.objects.filter(id__in=[a.id for a in accepted_articles]).update(status="accepted")
        Article.objects.filter(id__in=[a.id for a in rejected_articles]).update(status="rejected")
        
        response_data = {
            "session": session.title,
            "capacity": session.capacity,
            "percentage": percentage,
            "total_articles": total_articles,
            "accepted_count": len(accepted_articles),
            "rejected_count": len(rejected_articles),
            "accepted_articles": [
                {"id": a.id, "title": a.title, "avg_score": a.avg_score} for a in accepted_articles
            ],
            "rejected_articles": [
                {"id": a.id, "title": a.title, "avg_score": a.avg_score} for a in rejected_articles
            ],
        }
        return JsonResponse(response_data, status=200)
    

class ScoreThresholdSelectionAPI(APIView):
    """
    Acepta todos los artículos que tienen un puntaje promedio superior
    a un valor de corte definido en la solicitud.

    Ejemplo: 
    {
    "cutoff_score": 7.5
    }
    """

    def post(self, request, session_id):
        # Obtener el valor de corte (cutoff score)
        cutoff_score = request.data.get("cutoff_score")
        if cutoff_score is None:
            return JsonResponse(
                {"error": "Debe proporcionar un valor de corte (cutoff_score)."},
                status=400
            )

        try:
            cutoff_score = float(cutoff_score)
        except ValueError:
            return JsonResponse(
                {"error": "El valor de corte debe ser un número válido."},
                status=400
            )

        if not (-3 <= cutoff_score <= 3):
                    return JsonResponse(
                        {"error": "El valor de corte debe estar entre -3 y 3."},
                        status=400
                    )

        # Buscar la sesión
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({"error": "Sesión no encontrada."}, status=404)

        # Verificar si tiene artículos
        articles = (
            Article.objects.filter(session=session)
            .annotate(avg_score=Avg("review__score"))
            .exclude(avg_score=None)
        )

        if not articles.exists():
            return JsonResponse(
                {"message": "No hay artículos con puntajes disponibles para esta sesión."},
                status=200
            )

        # Seleccionar según el valor de corte
        accepted_articles = articles.filter(avg_score__gt=cutoff_score)
        rejected_articles = articles.exclude(avg_score__gt=cutoff_score)

        # Actualizar estados
        Article.objects.filter(id__in=[a.id for a in accepted_articles]).update(status="accepted")
        Article.objects.filter(id__in=[a.id for a in rejected_articles]).update(status="rejected")

        # Preparar respuesta
        response_data = {
            "session": session.title,
            "cutoff_score": cutoff_score,
            "total_articles": articles.count(),
            "accepted_count": accepted_articles.count(),
            "rejected_count": rejected_articles.count(),
            "accepted_articles": [
                {"id": a.id, "title": a.title, "avg_score": a.avg_score}
                for a in accepted_articles
            ],
            "rejected_articles": [
                {"id": a.id, "title": a.title, "avg_score": a.avg_score}
                for a in rejected_articles
            ],
        }

        return JsonResponse(response_data, status=200)


class ArticleReviewsAPI(APIView):
    """
    Devuelve todas las revisiones recibidas por un artículo,
    incluyendo datos del revisor.
    """

    def get(self, request, article_id):
        # Verificar si el artículo existe
        article = get_object_or_404(Article, id=article_id)

        # Buscar las reviews asociadas
        reviews = (
            Review.objects
            .filter(article=article)
            .select_related("reviewer")    # Optimiza acceso al revisor
        )

        if not reviews.exists():
            return JsonResponse(
                {"message": "Este artículo no tiene revisiones aún."},
                status=200
            )

        # Armar la respuesta
        result = [
            {
                "review_id": r.id,
                "reviewer": {
                    "id": r.reviewer.id,
                    "full_name": r.reviewer.full_name,
                    "email": r.reviewer.email
                },
                "score": r.score,
                "opinion": r.opinion,
            }
            for r in reviews
        ]

        return JsonResponse(result, safe=False, status=200)


class ReviewedArticlesWithStatusAPI(APIView):
    """
    Devuelve la lista de artículos aceptados o rechazados de una sesión
    """
    def get(self, request, session_id):
        # Captura el parámetro status de la URL (ej: ?status=accepted)
        status = request.query_params.get('status') 
        
        if status not in ['accepted', 'rejected']:
            return JsonResponse(
                {"error": "El parámetro status debe ser 'accepted' o 'rejected'."}, 
                status=400
            )

        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'error': 'Sesión no encontrada'}, status=404)

        articles = (
            Article.objects.filter(session=session, status=status)
            .annotate(avg_score=Avg("review__score"))
            .exclude(avg_score=None) 
            .order_by('-avg_score') 
        )

        response_data = [
            {
                "id": a.id,
                "title": a.title,
                "avg_score": a.avg_score, 
                "status": a.status,
            }
            for a in articles
        ]

        return JsonResponse(response_data, safe=False, status=200)


class ReviewedArticlesAPI(APIView):
    """
    Devuelve lista de artículos que tienen al menos una revisión publicada.
    """

    def get(self, request):
        # Buscar artículos con reviews publicadas
        articles = (
            Article.objects
            .filter(review__is_published=True)
            .annotate(review_count=Count("review"))
            .distinct()
        )

        result = [
            {
                "id": a.id,
                "title": a.title,
                "review_count": a.review_count,
            }
            for a in articles
        ]

        return Response(result, status=200)