from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    affiliation = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    roles = models.JSONField(default=list)
