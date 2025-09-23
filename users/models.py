from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Manager para el modelo User donde el email es el identificador único.
    """
    def create_user(self, email, password, full_name, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        if not full_name:
            raise ValueError(_("The Full Name must be set"))
            
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, full_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
            
        return self.create_user(email, password, full_name, **extra_fields)

class User(AbstractUser):
    """
    Modelo de Usuario personalizado para ComfyChair.
    """
    full_name = models.CharField(_("Full Name"), max_length=255)
    affiliation = models.CharField(_("Affiliation"), max_length=255, blank=True)
    email = models.EmailField(_("Email Address"), unique=True)
    is_author = models.BooleanField(default=True)
    is_reviewer = models.BooleanField(default=False)
    is_chair = models.BooleanField(default=False)
    
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    # Se asigna el manager definido justo arriba.
    objects = UserManager()

    # Campos para resolver el conflicto de migraciones
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_permissions_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.email