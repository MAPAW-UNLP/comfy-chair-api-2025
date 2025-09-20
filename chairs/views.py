from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Bidding
from articles.models import Article
from django.contrib.auth import get_user_model

Usuario = get_user_model()

@api_view(['GET'])
def get_revisores_disponibles(request, articulo_id):
    articulo = get_object_or_404(Article, pk=articulo_id)
    
    bids = Bidding.objects.filter(articulo=articulo).select_related('revisor')

    revisores_por_interes = {
        'interesados': [],
        'quizas': [],
        'no_interesados': []
    }

    for bid in bids:
        data_revisor = {
            'id': bid.revisor.id,
            'nombre_completo': bid.revisor.nombre_completo,
            'email': bid.revisor.email,
        }
        if bid.interes == 'interesado':
            revisores_por_interes['interesados'].append(data_revisor)
        elif bid.interes == 'quizas':
            revisores_por_interes['quizas'].append(data_revisor)
        elif bid.interes == 'no_interesado':
            revisores_por_interes['no_interesados'].append(data_revisor)

    return Response(revisores_por_interes)