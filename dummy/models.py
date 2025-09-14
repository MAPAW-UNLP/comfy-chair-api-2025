from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Dummy(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=150)
    apellido = models.CharField(max_length=100)
    afiliacion = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  #identificador único
    REQUIRED_FIELDS = ["username", "nombre_completo", "apellido","afiliacion"]

    def __str__(self):
        return f"{self.nombre_completo} {self.apellido} ({self.email})"
