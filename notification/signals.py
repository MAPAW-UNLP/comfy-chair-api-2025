from django.db.models.signals import post_save
from django.dispatch import receiver
from article.models import Article
from reviewer.models import Review, Bid
from .models import Notification
from chair.models import ReviewAssignment
from django.db.models.signals import m2m_changed
from conference.models import Conference
from conference_session.models import Session

# Notifica cuando se crea o modifica un articulo
@receiver(post_save, sender=Article)
def article_created_or_updated_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.corresponding_author,
            article=instance,
            title="Artículo enviado",
            message=f"Has enviado el artículo '{instance.title}' correctamente.",
            type="info"
        )
    else:
        Notification.objects.create(
            user=instance.corresponding_author,
            article=instance,
            title="Artículo modificado",
            message=f"Has modificado correctamente el artículo '{instance.title}'.",
            type="success"
        )

# Notifica cuando se le asigna o elimina una revision
@receiver(post_save, sender=ReviewAssignment)
def review_assignment_changed_notification(sender, instance, created, **kwargs):
    if created:
        # Nueva asignación
        Notification.objects.create(
            user=instance.reviewer,
            article=instance.article,
            title="Revisión asignada",
            message=f"Se te ha asignado revisar el artículo '{instance.article.title}'.",
            type="info"
        )
    elif instance.deleted:
        # Asignación eliminada (soft delete)
        Notification.objects.create(
            user=instance.reviewer,
            article=instance.article,
            title="Revisión designada",
            message=f"Ya no estás asignado para revisar el artículo '{instance.article.title}'.",
            type="warning"
        )

# Notifica cuando un revisor hace un bidding sobre un artículo o lo modifica
@receiver(post_save, sender=Bid)
def bid_created_or_updated_notification(sender, instance, created, **kwargs):
    if created:
        # El revisor realiza un nuevo bidding
        Notification.objects.create(
            user=instance.reviewer,
            article=instance.article,
            title="Bidding realizado",
            message=f"Has indicado tu interés '{instance.choice}' sobre el artículo '{instance.article.title}'.",
            type="info"
        )
    else:
        # El revisor modifica su bidding existente
        Notification.objects.create(
            user=instance.reviewer,
            article=instance.article,
            title="Bidding actualizado",
            message=f"Has cambiado tu interés a '{instance.choice}' para el artículo '{instance.article.title}'.",
            type="info"
        )

# Notifica al usuario cuando se le asigna ser chair general de una conferencia
@receiver(m2m_changed, sender=Conference.chairs.through)
def chair_assigned_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":  # cuando se agregan nuevos chairs
        for user_id in pk_set:
            Notification.objects.create(
                user_id=user_id,
                title="Asignado como Chair General",
                message=f"Has sido asignado como chair general de la conferencia '{instance.title}'.",
                type="info"
            )


# Notifica al usuario cuando se le asigna ser chair de una sesión
@receiver(m2m_changed, sender=Session.chairs.through)
def session_chair_assigned_notification(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        for user_id in pk_set:
            Notification.objects.create(
                user_id=user_id,
                title="Asignado como Chair de Sesión",
                message=f"Has sido asignado como chair de la sesión '{instance.title}' "
                        f"perteneciente a la conferencia '{instance.conference.title}'.",
                type="info"
            )