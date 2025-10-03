from django.db import models
from conference_sessions.models import Session
from users.models import User

class Article(models.Model):
    STATUS_CHOICES = [
        ('reception', 'Recepción'),
        ('bidding', 'Bidding'),
        ('assignment', 'Asignación'),
        ('review', 'Revisión'),
        ('selection', 'Selección'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
    ]

    ARTICLE_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('poster', 'Poster'),
    ]

    title = models.CharField(max_length=200)
    main_file_url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reception')
    article_type = models.CharField(max_length=10, choices=ARTICLE_TYPE_CHOICES)

    # Campos específicos
    abstract = models.TextField(blank=True, null=True)  # para Regular
    source_file_url = models.URLField(blank=True, null=True)  # para Poster

    # Relaciones
    authors = models.ManyToManyField(User, related_name='articles')
    notification_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notification_articles')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='articles', null=True, blank=True)

    def __str__(self):
        return self.title

