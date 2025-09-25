from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.username
