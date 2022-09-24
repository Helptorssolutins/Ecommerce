import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import DefaultUserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=80)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=80)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = DefaultUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
