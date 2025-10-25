from django.db import models
from django.contrib.auth import get_user_model
from article.models import Article
from user.models import User

class ReviewAssignment(models.Model):
    reviewer = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='assignment_reviews'
    )
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reviewer', 'article')
