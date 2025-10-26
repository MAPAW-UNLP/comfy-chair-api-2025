from django.db.models.signals import post_save
from django.dispatch import receiver
from article.models import Article
from reviewer.models import AssignmentReview, Review, Bid
from .models import Notification
from chair.models import ReviewAssignment

# Notifica cuando se crea un articulo
@receiver(post_save, sender=Article)
def article_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.corresponding_author,
            article=instance,
            title="Artículo enviado",
            message=f"Has enviado el artículo '{instance.title}' correctamente.",
            type="info"
        )

# Notifica cuando se asigna una revision
@receiver(post_save, sender=ReviewAssignment)
def review_assigned_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.reviewer,
            article=instance.article,
            title="Revisión asignada",
            message=f"Se te ha asignado revisar el artículo '{instance.article.title}'.",
            type="info"
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
