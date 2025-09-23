from django.db import models
from django.utils.translation import gettext_lazy as _

class User(models.Model):
    full_name = models.CharField(_("Nombre Completo"), max_length=255)
    affiliation = models.CharField(_("Afiliación"), max_length=255, blank=True)
    email = models.EmailField(_("Email"), unique=True)
    password = models.CharField(_("Contraseña"), max_length=128)

    # --- Roles del Usuario ---
    is_author = models.BooleanField(default=True)
    is_reviewer = models.BooleanField(default=False)
    is_chair = models.BooleanField(default=False)
    

    def __str__(self):
        return self.email