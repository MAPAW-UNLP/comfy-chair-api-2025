from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from chairs.models import ReviewAssignment, Bid
from chairs.serializers import ReviewAssignmentSerializer
from articles.models import Article
from users.models import User
import math


class ChairsAPI(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Chairs endpoint working!'})


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
            defaults={"is_active": True},
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
                is_active=True
            )
        except ReviewAssignment.DoesNotExist:
            return JsonResponse({'error': 'Reviewer not assigned or already inactive'}, status=404)

        review.is_active = False
        review.save()
        return JsonResponse({'message': 'Reviewer assignment logically deleted'}, status=200)


class AvailableReviewersAPI(APIView):
    """
    Devuelve una lista de revisores disponibles y priorizados para un artículo.
    1. Filtra revisores que no hayan alcanzado su límite de asignaciones.
    2. Ordena los candidatos según el interés.
    """

    def get(self, request, article_id):
        limit_reviews = math.ceil(
            Article.objects.count() * 3 / User.objects.filter(is_reviewer=True).count()
        )
        article = get_object_or_404(Article, pk=article_id)

        available_reviewers_by_load = User.objects.annotate(
            num_assignments=Count('assignment_reviews')
        ).filter(num_assignments__lt=limit_reviews)

        ids_available_reviewers = [rev.id for rev in available_reviewers_by_load]

        bids = Bid.objects.filter(
            article=article,
            reviewer_id__in=ids_available_reviewers
        ).select_related('reviewer')

        interested, maybe, not_interested = [], [], []
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
                    is_active=True
                ).exists(),
            }
            if bid.interest == 'interested':
                interested.append(reviewer_data)
            elif bid.interest == 'maybe':
                maybe.append(reviewer_data)
            elif bid.interest == 'not_interested':
                not_interested.append(reviewer_data)

        none_interest = []
        reviewers_without_bid = available_reviewers_by_load.exclude(id__in=reviewers_with_bid_ids)
        for reviewer in reviewers_without_bid:
            none_interest.append({
                'id': reviewer.id,
                'full_name': reviewer.full_name,
                'email': reviewer.email,
                'interest': 'none',
                'assigned': ReviewAssignment.objects.filter(
                    article=article,
                    reviewer=reviewer,
                    is_active=True
                ).exists(),
            })

        final_reviewer_list = []
        final_reviewer_list.extend(interested)
        if len(final_reviewer_list) < 3:
            final_reviewer_list.extend(maybe)
        if len(final_reviewer_list) < 3:
            final_reviewer_list.extend(none_interest)
        if len(final_reviewer_list) < 3:
            final_reviewer_list.extend(not_interested)

        # Ordena los revisores priorizando los no asignados
        final_reviewer_list = sorted(final_reviewer_list, key=lambda r: not r['assigned'])
        return JsonResponse(final_reviewer_list, safe=False)
