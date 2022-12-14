from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


class DefaultUserManager(BaseUserManager):
    # function to validate email
    def check_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address!!"))

    # create user
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not first_name:
            raise ValueError(_("Users must have a first name"))
        if not last_name:
            raise ValueError(_("Users must have a last name"))
        if email:
            email = self.normalize_email(email)
            self.check_email(email)
        else:
            raise ValueError(_("An email address is required"))

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save()
        return user

    # create superuser
    def create_superuser(self, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser should be a staff"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        if not password:
            raise ValueError(_("Superuser must have a password"))
        if email:
            email = self.normalize_email(email)
            self.check_email(email)
        else:
            raise ValueError(_("An email address is required"))
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        user.save()
        return user
