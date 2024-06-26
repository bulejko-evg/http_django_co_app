from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
)
from app.vendors.base.model import (
    BaseModel,
    BaseQuerySet,
)
from app.vendors.mixins.model import (
    TimestampsMixin,
    SoftDeleteMixin,
    RolePermissionsMixin,
)
from typing import (
    Tuple,
    List,
)


class AccountManager(BaseUserManager):
    """Custom account model manager."""
    def create_user(self, username, email, password, **extra_fields):
        """Create and save a user with username, email, password."""
        self._check(username, email, password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with username, email, password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, email, password, **extra_fields)
    
    def _check(self, username, email, password) -> None:
        """Check username, email, password of account."""
        pass


class Account(TimestampsMixin, SoftDeleteMixin, RolePermissionsMixin, AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model."""
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
    is_confirmed = models.BooleanField(
        default=False
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
    
    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]
    
    def delete(self, soft=False, **kwargs) -> None:
        """Delete or soft delete account"""
        if soft is True:
            self.is_active = False
        super().delete(soft=soft, **kwargs)
    
    def is_actual(self) -> Tuple[bool, List[str]]:
        """Get (tuple) is the model item actual (bool, active and confirmed), with fail messages (list[str])"""
        is_actual, fail_messages = super().is_actual()
        if self.is_active is not None:
            is_actual = False
            fail_messages.append(_("Not active"))
        if self.is_confirmed is not None:
            is_actual = False
            fail_messages.append(_("Not confirmed"))
        
        return is_actual, fail_messages
    
    _permissions = {}