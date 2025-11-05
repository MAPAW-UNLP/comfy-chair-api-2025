from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from user.models import User
from conference.models import Conference
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

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
    # opcionales
    threshold_percentage = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True,
        default=None
    )
    improvement_threshold = models.FloatField(
        validators=[
            MinValueValidator(-3),
            MaxValueValidator(3)
        ],
        null=True,
        blank=True,
        default=None
    )

    chairs = models.ManyToManyField(
        User,
        blank=True,
        related_name='session'
    )

    def __str__(self):
        return f"{self.title} ({self.conference.title})"

    def clean(self):
        # Validar que el deadline esté dentro del rango de la conferencia
        if self.conference and self.deadline:
            start = self.conference.start_date
            end = self.conference.end_date
            if start and end and (self.deadline < start or self.deadline > end):
                raise ValidationError({
                    'deadline': 'La fecha de deadline debe estar entre las fechas de inicio y fin de la conferencia.'
                })

    def save(self, *args, **kwargs):
        # ejecutar validaciones de modelo antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            # Título único por conferencia no distinguimos mayúsculas/minúsculas
            UniqueConstraint(
                Lower('title'), 
                'conference', 
                name='unique_session_title_per_conference_ci'
            )
        ]
