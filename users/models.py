from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    affiliation = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('chair', 'Chair'),
        ('reviewer', 'Reviewer'),
        ('author', 'Author'),
    ]
    roles = models.ManyToManyField('Role', blank=True)

class Role(models.Model):
    name = models.CharField(max_length=50, choices=User.ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name
