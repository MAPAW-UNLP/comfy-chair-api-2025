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

# por ahora pongo un nro fijo random, pero va a depender del modelo Session cuando exista

@api_view(['GET'])
def get_available_reviewers(request, article_id):
    """
    Devuelve una lista de revisores disponibles y priorizados para un artículo.
    1. Filtra revisores que no hayan alcanzado su límite de asignaciones.
    2. Ordena los candidatos según el interés:
       - Primero, todos los 'interesados'.
       - Si no se llega a 3, se añaden todos los 'quizas'.
       - Si aún no se llega a 3, se añaden los que no opinaron ('ninguno').
       - Finalmente, si es necesario, se recurre a los 'no_interesado'.
    """
    limit_reviews = math.ceil(Article.objects.count() * 3 / User.objects.filter(is_reviewer=True).count())
    article = get_object_or_404(Article, pk=article_id)

    available_reviewers_by_load = User.objects.annotate(
        num_assignments=Count('assignmentreviews')
    ).filter(num_assignments__lt=limit_reviews)

    ids_available_reviewers = [rev.id for rev in available_reviewers_by_load]

    bids = Bidding.objects.filter(
        article=article,
        reviewer_id__in=ids_available_reviewers
    ).select_related('reviewer')

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
            'interes': bid.interest
        }
        if bid.interest == 'interesado':
            interesados.append(data_reviewer)
        elif bid.interest == 'quizas':
            quizas.append(data_reviewer)
        elif bid.interest == 'no_interesado':
            no_interesados.append(data_reviewer)

    ninguno = []
    revisores_sin_bid = available_reviewers_by_load.exclude(id__in=ids_reviewers_with_bid)
    for reviewer in revisores_sin_bid:
        ninguno.append({
            'id': reviewer.id,
            'nombre_completo': reviewer.full_name,
            'email': reviewer.email,
            'interes': 'ninguno'
        })

    lista_final_revisores = []
    
    lista_final_revisores.extend(interesados)
    
    if len(lista_final_revisores) < 3:
        lista_final_revisores.extend(quizas)

    if len(lista_final_revisores) < 3:
        lista_final_revisores.extend(ninguno)

    if len(lista_final_revisores) < 3:
        lista_final_revisores.extend(no_interesados) 
    return Response(lista_final_revisores)