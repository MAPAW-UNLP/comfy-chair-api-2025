from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ("user", "User"),
        ("admin", "Admin")
    )
    full_name = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES)
    deleted = models.BooleanField(default=False)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "affiliation"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"