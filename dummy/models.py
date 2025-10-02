from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Dummy(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    name = models.CharField(max_length=100)
    
class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    
class Bid(models.Model):
    STATES = ["Interesado", "No Interesado", "Quizás"]
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    choice = models.CharField(max_length=20, choices=STATES, null=True, blank=True)