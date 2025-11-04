from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from user.models import User

class Conference (models.Model):

    VISTA_CHOICES = [
        ('single blind', 'Single blind'),
        ('double blind', 'Double blind'),
        ('completo', 'Completo')
    ]
    
    title = models.CharField(max_length=50)

    description = models.CharField(max_length=300)
    start_date = models.DateField(
        null=False, 
        blank=False
    )
    end_date = models.DateField(
        null=False, 
        blank=False
    )
    # tipo de lectura 
    blind_kind = models.CharField(
        max_length=12,
        choices=VISTA_CHOICES,
        default='completo'
    )
    
    # lista de chairs
    chairs = models.ManyToManyField(
        User,
        blank=True,
        related_name='conferences'
    )
    
    def __str__(self):
        return self.title

    class Meta:
        # la conferencia no acepta títulos duplicados no distinguimos mayúsculas/minúsculas
        constraints = [
            UniqueConstraint(
                Lower('title'),
                name='unique_conference_title_ci'
            )
        ]
