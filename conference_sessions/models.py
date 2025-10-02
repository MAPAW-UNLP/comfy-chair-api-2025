from django.db import models
from articles.models import Article  # Importamos Article para la relación ManyToMany

class ConferenceSession(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    articles = models.ManyToManyField(Article, related_name='conference_sessions')
    conference_title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
