from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article
from users.models import User


class Bidding(models.Model):
    INTERESES = (
        ('interesado', 'Interesado'),
        ('quizas', 'Quizás'),
        ('no_interesado', 'No Interesado'),
        ('ninguno', 'Ninguno'),
    )
    revisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    articulo = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bids')
    interes = models.CharField(max_length=20, choices=INTERESES, default='ninguno')

    class Meta:
        unique_together = ('revisor', 'articulo')

class AssignmentReview(models.Model):
    revisor = models.ForeignKey(User, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Article, on_delete=models.CASCADE)
    revisado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('revisor', 'articulo')

class Review(models.Model):
    revisor = models.ForeignKey(User, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Article, on_delete=models.CASCADE)
    texto = models.TextField()
    puntaje = models.IntegerField(choices=[(i, i) for i in range(-3, 4)])

    def __str__(self):
        return f"Revisión de {self.revisor.nombre_completo} para '{self.articulo.title}'"