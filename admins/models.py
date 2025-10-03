from django.db import models

class Conferencia (models.Model):

    VISTA_CHOICES = [
        ('single blind', 'Single blind'),
        ('double blind', 'Double blind'),
        ('completo', 'Completo')
    ]

    titulo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=300)
    fecha_ini = models.DateField(
        null=False,
        blank=False
    )
    fecha_fin = models.DateField(
        null=False,
        blank=False
    )
    # tipo de lectura que 
    vista = models.CharField(
        max_length=12,
        choices=VISTA_CHOICES,
        default='completo'
    )
    
    def __str__(self):
        return self.titulo
    