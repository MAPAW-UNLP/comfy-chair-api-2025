from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conferencia
from .serializers import ConferenciaSerializer

from django.utils import timezone

class ConferenciaViewSet(viewsets.ModelViewSet):
    queryset = Conferencia.objects.all().order_by('-id')
    serializer_class = ConferenciaSerializer

    # /api/conferencias/terminadas/  -->  devuelve las conferencias con fecha_fin < fecha_actual
    @action(detail=False, methods=['get'])
    def terminadas(self, request):
        fecha_actual = timezone.now().date()
        conferencias = Conferencia.objects.filter(fecha_fin__lt = fecha_actual)
        serializer = self.get_serializer(conferencias, many=True)
        return Response(serializer.data)
    
    # /api/conferencias/activas/ --> devuelve las conferencias con fecha_fin > fecha_actual
    @action(detail=False, methods=['get'])
    def activas(self, request):
        fecha_actual = timezone.now().date()
        conferencias = Conferencia.objects.filter(fecha_fin__gte = fecha_actual)
        serializer = self.get_serializer(conferencias, many=True)
        return Response(serializer.data)
