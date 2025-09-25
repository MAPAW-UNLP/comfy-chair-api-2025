from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ("user", "User"),
        ("admin", "Admin"),
    )
    nombre_completo = models.CharField(max_length=150)
    afiliacion = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)

    username = None  # Eliminamos el username

    USERNAME_FIELD = "email"  #identificador único
    REQUIRED_FIELDS = ["nombre_completo", "afiliacion"]

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"
