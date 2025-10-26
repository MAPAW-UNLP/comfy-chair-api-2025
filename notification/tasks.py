import time
from datetime import timedelta
from django.utils import timezone

def verificar_deadlines():
    """Revisa artículos y crea notificaciones si falta menos de 24h."""
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

           
            if timezone.is_naive(sesion.deadline):
                deadline_aware = timezone.make_aware(sesion.deadline)
            else:
                deadline_aware = sesion.deadline

            # Filtrar articulos dentro de las proximas 24h
            if ahora < deadline_aware <= dentro_24hs:
                # Evita duplicados
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
                        message=(
                            f"Tu artículo '{articulo.title}' tiene la sesión '{sesion.title}' "
                            f"que finaliza el {deadline_aware.strftime('%d/%m/%Y %H:%M')}. "
                            "Tenés menos de 24 horas para realizar modificaciones antes del cierre."
                        ),
                        type="critical",
                    )
                    #print(f"[Notificación creada] Autor: {autor.full_name} - Artículo: {articulo.title}")

        time.sleep(10)