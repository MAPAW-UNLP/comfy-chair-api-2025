from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Dummy(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Articulo(models.Model):
    nombre = models.CharField(max_length=100)
    
class Review(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    puntaje = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    
class Bid(models.Model):
    ESTADOS = ["Interesado", "No Interesado", "Quizás"]
    
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    
    estado =models.CharField(max_length=20, choices=ESTADOS, null=True, blank=True)