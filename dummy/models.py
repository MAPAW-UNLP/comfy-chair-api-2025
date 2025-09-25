from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Dummy(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=150)
    afiliacion = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    username = None  # Eliminamos el username

    USERNAME_FIELD = "email"  #identificador único
    REQUIRED_FIELDS = ["nombre_completo", "afiliacion"]

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"
