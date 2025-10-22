from django.db import models
from user.models import User
from conference.models import Conference
from django.core.validators import MinValueValidator, MaxValueValidator

class Session(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateField(
        null=False,
        blank=False
    )
    capacity = models.IntegerField(null=False, blank=False)
    conference = models.ForeignKey(
        Conference, 
        on_delete=models.CASCADE, 
        related_name='session'
    )
    threshold_percentage = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    improvement_threshold = models.IntegerField(
        validators=[
            MinValueValidator(-3),
            MaxValueValidator(3)
        ]
    )
    chairs = models.ManyToManyField(
        User,
        blank=True,
        related_name='session'
    )

    def __str__(self):
        return f"{self.title} ({self.conference.title})"
