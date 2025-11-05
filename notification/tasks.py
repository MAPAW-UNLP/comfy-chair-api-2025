from datetime import timedelta, datetime
from django.utils import timezone
import time

def verificar_deadlines():
    time.sleep(5)

    while True:
        from article.models import Article
        from notification.models import Notification

        ahora = timezone.now()
        dentro_24hs = ahora + timedelta(hours=24)

        articulos = Article.objects.select_related('session', 'corresponding_author')

        for articulo in articulos:
            autor = articulo.corresponding_author
            sesion = articulo.session
            if not autor or not sesion or not sesion.deadline:
                continue

            # Asegurar que sea datetime con zona horaria
            if isinstance(sesion.deadline, datetime):
                deadline_dt = sesion.deadline
            else:
                deadline_dt = datetime.combine(sesion.deadline, datetime.min.time())

            if timezone.is_naive(deadline_dt):
                deadline_aware = timezone.make_aware(deadline_dt)
            else:
                deadline_aware = deadline_dt

            diff = (deadline_aware - ahora).total_seconds()

            if 0 <= diff <= 86400:  # dentro de 24h
                existe = Notification.objects.filter(
                    user=autor,
                    article=articulo,
                    title__icontains="deadline de la sesión"
                ).exists()

                if not existe:
                    Notification.objects.create(
                        user=autor,
                        article=articulo,
                        title=f"Se aproxima el deadline de la sesión '{sesion.title}'",
                        message=(f"Tu artículo '{articulo.title}' tiene la sesión '{sesion.title}' "
                                 f"que finaliza el {deadline_aware.strftime('%d/%m/%Y %H:%M')}. "
                                 "Tenés menos de 24 horas para realizar modificaciones antes del cierre."),
                        type="info",
                    )
                    #print(f"[Notificación creada] Autor: {autor.full_name} - Artículo: {articulo.title}")
            else:
                print(f"[Fuera de rango] {articulo.title} - Deadline {deadline_aware}")

        time.sleep(10)