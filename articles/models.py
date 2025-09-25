from django.db import models
from users.models import User

class Article(models.Model):
    TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('poster', 'Poster'),
    ]

    title = models.CharField(max_length=200)
    file_url = models.URLField()
    abstract = models.TextField(blank=True)
    article_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    authors = models.ManyToManyField(User, related_name='articles')
    notification_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    status = models.CharField(max_length=20, default='in_reception')

    def __str__(self):
        return self.title
