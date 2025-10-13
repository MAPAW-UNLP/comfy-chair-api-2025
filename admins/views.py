from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conference
from .serializers import ConferenciaSerializer

from django.utils import timezone

class ConferenciaViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all().order_by('-id')
    serializer_class = ConferenciaSerializer

    # /api/conferencias/terminadas/  -->  devuelve las conferencias con end_date < fecha_actual
    @action(detail=False, methods=['get'])
    def terminadas(self, request):
        fecha_actual = timezone.now().date()
        conferencias = Conference.objects.filter(
            end_date__lt=fecha_actual
        ).order_by('-id')  
        serializer = self.get_serializer(conferencias, many=True)
        return Response(serializer.data)
    
    # /api/conferencias/activas/ --> devuelve las conferencias con end_date >= fecha_actual
    @action(detail=False, methods=['get'])
    def activas(self, request):
        fecha_actual = timezone.now().date()
        conferencias = Conference.objects.filter(
            end_date__gte=fecha_actual
        ).order_by('-id') 
        serializer = self.get_serializer(conferencias, many=True)
        return Response(serializer.data)