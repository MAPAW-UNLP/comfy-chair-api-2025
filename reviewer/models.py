from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
#Eliminar despues:
class AssignmentReview(models.Model):
    reviewer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assignmentreviews'
    )
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reviewer', 'article')

class User(models.Model):
    full_name = models.CharField(_("Nombre Completo"), max_length=255)
    affiliation = models.CharField(_("Afiliación"), max_length=255, blank=True)
    email = models.EmailField(_("Email"), unique=True)
    password = models.CharField(_("Contraseña"), max_length=128)
    
    is_author = models.BooleanField(default=True)
    is_reviewer = models.BooleanField(default=False)
    is_chair = models.BooleanField(default=False)
    

    def __str__(self):
        return self.email
    
class Review(models.Model):
    reviewer = models.ForeignKey('auth.User')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(-3), MaxValueValidator(3)]
    )
    opinion = models.TextField()
    
class Bid(models.Model):
    STATES = ["Interesado", "No Interesado", "Quizás"]
    
    reviewer = models.ForeignKey('auth.User')
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    choice = models.CharField(max_length=20, choices=STATES, null=True, blank=True)