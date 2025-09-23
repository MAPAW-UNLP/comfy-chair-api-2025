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
def get_revisores_disponibles(request, articulo_id):
    """
    Devuelve una lista de revisores disponibles y priorizados para un artículo.
    1. Filtra revisores que no hayan alcanzado su límite de asignaciones.
    2. Ordena los candidatos según el interés:
       - Primero, todos los 'interesados'.
       - Si no se llega a 3, se añaden todos los 'quizas'.
       - Si aún no se llega a 3, se añaden los que no opinaron ('ninguno').
       - Finalmente, si es necesario, se recurre a los 'no_interesado'.
    """
    limite_revisiones = math.ceil(Article.objects.count() * 3 / User.objects.filter(is_reviewer=True).count())
    articulo = get_object_or_404(Article, pk=articulo_id)

    # 1. Obtenemos los revisores que aún tienen capacidad para revisar.
    revisores_disponibles_por_carga = Usuario.objects.annotate(
        num_asignaciones=Count('assignmentreview')
    ).filter(num_asignaciones__lt=limite_revisiones)
    
    # IDs de los revisores que cumplen el requisito de carga
    ids_revisores_disponibles = [rev.id for rev in revisores_disponibles_por_carga]

    # 2. Obtenemos todos los bids del artículo para los revisores disponibles
    bids = Bidding.objects.filter(
        articulo=articulo,
        revisor_id__in=ids_revisores_disponibles
    ).select_related('revisor')

    # 3. Clasificamos los revisores en sus respectivas categorías
    interesados = []
    quizas = []
    no_interesados = []
    
    ids_revisores_con_bid = [] # Para saber quiénes ya opinaron

    for bid in bids:
        ids_revisores_con_bid.append(bid.revisor.id)
        data_revisor = {
            'id': bid.revisor.id,
            'nombre_completo': bid.revisor.nombre_completo,
            'email': bid.revisor.email,
            'interes': bid.interes
        }
        if bid.interes == 'interesado':
            interesados.append(data_revisor)
        elif bid.interes == 'quizas':
            quizas.append(data_revisor)
        elif bid.interes == 'no_interesado':
            no_interesados.append(data_revisor)
            
    # Identificamos a los que no opinaron (interés 'ninguno' o sin bid)
    ninguno = []
    revisores_sin_bid = revisores_disponibles_por_carga.exclude(id__in=ids_revisores_con_bid)
    for revisor in revisores_sin_bid:
        ninguno.append({
            'id': revisor.id,
            'nombre_completo': revisor.nombre_completo,
            'email': revisor.email,
            'interes': 'ninguno'
        })

    # 4. Construimos la lista final siguiendo la lógica de inclusión por grupos
    lista_final_revisores = []
    
    # Añadir todos los interesados
    lista_final_revisores.extend(interesados)
    
    # Si no se llega a 3, añadir todos los 'quizás'
    if len(lista_final_revisores) < 3:
        lista_final_revisores.extend(quizas)
        
    # Si aún no se llega a 3, añadir todos los que no indicaron interés
    if len(lista_final_revisores) < 3:
        lista_final_revisores.extend(ninguno)

    # Si sigue sin llegarse a 3, añadir todos los 'no interesados'
    if len(lista_final_revisores) < 3:
        lista_final_revisores.extend(no_interesados)

    return Response(lista_final_revisores)