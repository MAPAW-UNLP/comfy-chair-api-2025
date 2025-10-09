from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Bidding, AssignmentReview
from articles.models import Article
from django.contrib.auth import get_user_model
import math
from articles.models import *
from users.models import *

Usuario = get_user_model()

@api_view(['GET'])
def get_available_reviewers(request, article_id):
    """
    Devuelve todos los revisores disponibles y asignados, priorizados según el interés.
    """
    article = get_object_or_404(Article, pk=article_id)

    bids = Bidding.objects.filter(article=article).select_related('reviewer')

    interesados = []
    quizas = []
    no_interesados = []
    
    ids_reviewers_with_bid = []

    for bid in bids:
        ids_reviewers_with_bid.append(bid.reviewer.id)
        data_reviewer = {
            'id': bid.reviewer.id,
            'nombre_completo': bid.reviewer.full_name,
            'email': bid.reviewer.email,
            'interes': bid.interest,
            'asignado': AssignmentReview.objects.filter(article=article, reviewer=bid.reviewer, is_active=True).exists(),
        }
        if bid.interest == 'interesado':
            interesados.append(data_reviewer)
        elif bid.interest == 'quizas':
            quizas.append(data_reviewer)
        elif bid.interest == 'no_interesado':
            no_interesados.append(data_reviewer)

    revisores_sin_bid = User.objects.filter(is_reviewer=True).exclude(id__in=ids_reviewers_with_bid)
    ninguno = [
        {
            'id': reviewer.id,
            'nombre_completo': reviewer.full_name,
            'email': reviewer.email,
            'interes': 'ninguno',
            'asignado': AssignmentReview.objects.filter(article=article, reviewer=reviewer, is_active=True).exists(),
        }
        for reviewer in revisores_sin_bid
    ]

    lista_final_revisores = []
    lista_final_revisores.extend(interesados)
    lista_final_revisores.extend(quizas)
    lista_final_revisores.extend(ninguno)
    lista_final_revisores.extend(no_interesados)

    lista_final_revisores = sorted(lista_final_revisores, key=lambda r: not r['asignado'])

    return Response(lista_final_revisores)
