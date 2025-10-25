from django.db import models
from user.models import User
from article.models import Article

class ReviewScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_scores')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='review_scores')
    score = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        unique_together = ('user', 'article')
        verbose_name_plural = "review_scores"

    def __str__(self):
        return f"{self.user.email} → {self.article.title}: {self.score}"
