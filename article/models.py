from django.db import models
from conference_session.models import Session
from user.models import User

class Article(models.Model):

    # Tipos de Articulos
    ARTICLE_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('poster', 'Poster'),
    ]

    # Estados posibles de un Articulo
    STATUS_CHOICES = [
        ('reception', 'Recepción'),
        ('bidding', 'Bidding'),
        ('assignment', 'Asignación'),
        ('review', 'Revisión'),
        ('selection', 'Selección'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
    ]

    # Atributos (Adaptados Para el Primer Merge)
    title = models.CharField(max_length=200)
    main_file = models.FileField(upload_to='articles/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reception')
    type = models.CharField(max_length=10, choices=ARTICLE_TYPE_CHOICES)
    abstract = models.TextField(max_length=300)
    source_file = models.FileField(upload_to='articles/sources/', blank=True, null=True)  # Solo para Articulos de Tipo Poster

    # Relaciones 
    authors = models.ManyToManyField(User, related_name='article')
    corresponding_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notification_article')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='article', null=True, blank=True)

    def __str__(self):
        return self.title

