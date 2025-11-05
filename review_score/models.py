from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User
from article.models import Article

class ReviewScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_scores')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='review_scores')
    score = models.IntegerField(
        validators=[
            MinValueValidator(-3),
            MaxValueValidator(3)
        ]
    )

    class Meta:
        unique_together = ('user', 'article')
        verbose_name_plural = "review_scores"

    def __str__(self):
        return f"{self.user.email} → {self.article.title}: {self.score}"
