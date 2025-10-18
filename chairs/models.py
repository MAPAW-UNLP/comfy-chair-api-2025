from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article
from users.models import User

class ReviewAssignment(models.Model):
    reviewer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assignment_reviews'
    )
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=True)

    class Meta:
        unique_together = ('reviewer', 'article')
