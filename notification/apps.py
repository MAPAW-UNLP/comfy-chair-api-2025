from django.apps import AppConfig
import os
import threading

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    def ready(self):
        import notification.signals

        # Evita ejecutar dos veces con runserver autoreload
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from notification.tasks import verificar_deadlines
        threading.Thread(target=verificar_deadlines, daemon=True).start()