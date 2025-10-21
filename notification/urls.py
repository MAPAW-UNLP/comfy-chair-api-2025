from django.urls import path
from .views import UserNotificationsAPI, MarkNotificationReadAPI

urlpatterns = [
    path('', UserNotificationsAPI.as_view(), name='user-notifications'),
    path('<int:pk>/read/', MarkNotificationReadAPI.as_view(), name='mark-notification-read'),
]