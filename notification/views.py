from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class UserNotificationsAPI(APIView):
    def get(self, request):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

        notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkNotificationReadAPI(APIView):
    def post(self, request, pk):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            notification = Notification.objects.get(id=pk, user_id=user_id)
        except Notification.DoesNotExist:
            return Response({'error': 'Notificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        notification.read = True
        notification.save()
        return Response({'message': 'Notificación marcada como leída'}, status=status.HTTP_200_OK)

