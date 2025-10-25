from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg
from rest_framework.views import APIView

from chair.models import ReviewAssignment
from chair.serializers import ReviewAssignmentSerializer
from reviewer.models import Bid, Review
from article.models import Article
from user.models import User
from conference_session.models import Session


class ChairAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Chair endpoint working!'})


class CreateReviewAssignmentAPI(APIView):
    def post(self, request):
        reviewer_id = request.data.get("reviewer")
        article_id = request.data.get("article")
        if not reviewer_id or not article_id:
            return JsonResponse(
                {"error": "Reviewer y Article son requeridos."}, status=400
            )
        article = get_object_or_404(Article, pk=article_id)
        reviewer = get_object_or_404(User, pk=reviewer_id)
        if article.status not in ["assignment", "review"]:
            return JsonResponse(
                {"error": "No se pueden asignar revisores en el estado actual del artículo."},
                status=400
            )
        if ReviewAssignment.objects.filter(article=article, reviewer=reviewer, deleted=False).exists():
            return JsonResponse(
                {"error": "Este revisor ya está asignado a este artículo."},
                status=400
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
        assignment = ReviewAssignment.objects.filter(
            article_id=article_id,
            reviewer_id=reviewer_id,
            deleted=False
        ).first()
        if not assignment:
            return JsonResponse({"error": "No existe una asignación activa para eliminar."}, status=404)
        if Review.objects.filter(article_id=article_id, reviewer_id=reviewer_id).exists():
            return JsonResponse(
                {"error": "No se puede eliminar un revisor que ya ha realizado una revisión."},
                status=400
            )
        assignment.deleted = True
        assignment.save()
        return JsonResponse({'message': 'Reviewer assignment logically deleted'}, status=200)


class AvailableReviewersAPI(APIView):
    """
    Devuelve todos los revisores disponibles y asignados, priorizados según el interés.
    Optimizado para evitar N+1 queries.
    """
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        if not article.session or article.session.status not in ["bidding", "assignment", "review"]:
            return JsonResponse(
                {"error": "El artículo no pertenece a una sesión activa."},
                status=400
            )
        bids = Bid.objects.filter(article=article).select_related('reviewer')
        assigned_reviewers_ids = set(
            ReviewAssignment.objects.filter(article=article, deleted=False)
            .values_list('reviewer_id', flat=True)
        )
        interested, maybe, not_interested = [], [], []
        reviewers_with_bid_ids = []
        for bid in bids:
            reviewers_with_bid_ids.append(bid.reviewer.id)
            reviewer_data = {
                'id': bid.reviewer.id,
                'full_name': bid.reviewer.full_name,
                'email': bid.reviewer.email,
                'interest': bid.interest,
                'assigned': bid.reviewer.id in assigned_reviewers_ids,
            }
            if bid.interest == 'interested':
                interested.append(reviewer_data)
            elif bid.interest == 'maybe':
                maybe.append(reviewer_data)
            elif bid.interest == 'not_interested':
                not_interested.append(reviewer_data)
        reviewers_without_bid = User.objects.filter(role="user").exclude(id__in=reviewers_with_bid_ids)
        none_interest = [
            {
                'id': reviewer.id,
                'full_name': reviewer.full_name,
                'email': reviewer.email,
                'interest': 'none',
                'assigned': reviewer.id in assigned_reviewers_ids,
            }
            for reviewer in reviewers_without_bid
        ]
        final_reviewer_list = interested + maybe + none_interest + not_interested
        final_reviewer_list = sorted(final_reviewer_list, key=lambda r: not r['assigned'])
        return JsonResponse(final_reviewer_list, safe=False)



class FixedCutoffSelectionAPI(APIView):
    def post(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'error': 'Sesión no encontrada'}, status=404)
        if session.status != "review":
            return JsonResponse(
                {"error": "Solo se puede ejecutar la selección en sesiones en estado 'review'."},
                status=400
            )
        if not session.capacity or session.capacity <= 0:
            return JsonResponse(
                {"error": "La sesión no tiene definida una capacidad válida."},
                status=400
            )
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
        cutoff_index = min(session.capacity, total_articles)
        accepted_articles = articles[:cutoff_index]
        rejected_articles = articles[cutoff_index:]
        Article.objects.filter(id__in=[a.id for a in accepted_articles]).update(status="accepted")
        Article.objects.filter(id__in=[a.id for a in rejected_articles]).update(status="rejected")
        session.status = "selection"
        session.save(update_fields=["status"])
        response_data = {
            "session": session.title,
            "new_status": session.status,
            "capacity": session.capacity,
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