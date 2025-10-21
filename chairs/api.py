from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from chairs.models import ReviewAssignment 
from reviewer.models import Bid
from chairs.serializers import ReviewAssignmentSerializer
from article.models import Article
from user.models import User


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
