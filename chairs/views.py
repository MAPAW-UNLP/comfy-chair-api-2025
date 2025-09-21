from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Bidding
from articles.models import Article
from django.contrib.auth import get_user_model

Usuario = get_user_model()

@api_view(['GET'])
def get_revisores_disponibles(request, articulo_id):
    """
    Devuelve una lista de revisores priorizada.
    - Muestra todos los 'interesados'.
    - Si hay menos de 3 'interesados', añade a todos los 'quizas'.
    - Si la suma de los anteriores es menor a 3, añade a todos los 'no_interesados'.
    """
    articulo = get_object_or_404(Article, pk=articulo_id)
    
    # Obtenemos todos los bids para el artículo de una sola vez
    bids = Bidding.objects.filter(articulo=articulo).select_related('revisor')

    # Clasificamos los revisores en sus respectivas categorías
    interesados = []
    quizas = []
    no_interesados = []

    for bid in bids:
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
    
    # Construimos la lista final siguiendo la lógica de inclusión por grupos
    revisores_disponibles = []
    
    # Añadir todos los interesados
    revisores_disponibles.extend(interesados)

    # Si no se llega a 3, añadir todos los 'quizás'
    if len(revisores_disponibles) < 3:
        revisores_disponibles.extend(quizas)

    # Si sigue sin llegarse a 3, añadir todos los 'no interesados'
    if len(revisores_disponibles) < 3:
        revisores_disponibles.extend(no_interesados)

    return Response(revisores_disponibles)