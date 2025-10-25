from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from article.models import Article
from user.models import User

class AssignmentReview(models.Model):
    reviewer = models.ForeignKey(
        'user.User',  # <-- referencia correcta
        on_delete=models.CASCADE,
        related_name='assignmentreviews'
    )
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)  # <-- referencia correcta
    reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reviewer', 'article')
    
class Review(models.Model):
    #reviewer = models.ForeignKey('auth.User')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    is_published = models.BooleanField(default=False)
    is_edited = models.BooleanField(default = False)
    published_at = models.DateTimeField(null=True, blank=True)
    last_updated_after_publication = models.DateTimeField(null=True, blank=True)
    
class Bid(models.Model):
    STATE_CHOICES = [
        ("Interesado", "Interesado"),
        ("No Interesado", "No Interesado"), 
        ("Quizás", "Quizás"),
        ("No_select", "No seleccionado"),  # <-- Agrega la etiqueta legible
    ]
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default="No_select",
        null=True,
        blank=True
    )