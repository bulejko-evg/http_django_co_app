from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    """Custom account model manager."""
    def create_user(self, username, email, password, **extra_fields):
        """Create and save a user with the given username, email, password."""
        self._check(username, email, password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with the given username, email, password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, email, password, **extra_fields)
    
    def _check(self, username, email, password) -> None:
        """Check account username, email, password"""
        pass


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=80,
        unique=True
    )
    email = models.EmailField(
        max_length=80,
        unique=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = AccountManager()

    def __str__(self) -> str:
        return self.username
    
    def __repr__(self) -> str:
        return self.username