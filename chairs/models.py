from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article
from users.models import User


class Bid(models.Model):
    # Intereses posibles del revisor respecto al artículo
    INTEREST_CHOICES = (
        ('interested', 'Interesado'),
        ('maybe', 'Quizás'),
        ('not_interested', 'No Interesado'),
        ('none', 'Ninguno'),
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bids')
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, default='none')

    class Meta:
        unique_together = ('reviewer', 'article')


class ReviewAssignment(models.Model):
    reviewer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assignment_reviews'
    )
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('reviewer', 'article')


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(choices=[(i, i) for i in range(-3, 4)])

    def __str__(self):
        return f"Review by {self.reviewer.full_name} for '{self.article.title}'"
