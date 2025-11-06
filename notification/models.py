from django.db import models
from user.models import User
from article.models import Article

class Notification(models.Model):
    TYPE_CHOICES = [
        ("info", "Informativa"),
        ("critical", "Crítica"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="info")
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.title} ({'leída' if self.read else 'no leída'})"


