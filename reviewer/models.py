from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from article.models import Article
from chair.models import ReviewAssignment
from user.models import User


    
class Review(models.Model):
    review_assignment = models.ForeignKey( ReviewAssignment, on_delete=models.CASCADE,related_name='reviews')
    score = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    #is_published = models.BooleanField(default=False)
    #is_edited = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewVersion(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,related_name='versions')
    version_number = models.IntegerField(default=1)
    score = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
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