from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article
from users.models import User


class Bidding(models.Model):
    INTERESES = (
        ('interesado', 'Interesado'),
        ('quizas', 'Quizás'),
        ('no_interesado', 'No Interesado'),
        ('ninguno', 'Ninguno'),
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bids')
    interest = models.CharField(max_length=20, choices=INTERESES, default='ninguno')

    class Meta:
        unique_together = ('reviewer', 'article')

class AssignmentReview(models.Model):
    reviewer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assignmentreviews'
    )
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reviewer', 'article')

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(choices=[(i, i) for i in range(-3, 4)])

    def __str__(self):
        return f"Revisión de {self.reviewer.full_name} para '{self.article.title}'"