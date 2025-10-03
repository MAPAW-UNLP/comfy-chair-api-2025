from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class Review(models.Model):
    reviewer = models.ForeignKey('auth.User')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    
class Bid(models.Model):
    STATES = ["Interesado", "No Interesado", "Quizás"]
    
    reviewer = models.ForeignKey('auth.User')
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    choice = models.CharField(max_length=20, choices=STATES, null=True, blank=True)