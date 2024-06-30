from django.db import models
from django.conf import settings
from django.contrib import admin as adm
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
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
from ..utils import (
    set_account_permissions, 
    account_token,
)
from app.vendors.helpers.validations import (
    is_username_valid,
    is_email_valid,
    is_password_valid,
    validate_username,
    validate_email,
    validate_password,
)
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)
from django.utils.encoding import (
    force_str,
    force_bytes,
)
from typing import (
    Tuple,
    List,
    Self,
)

from app.apps.company.models import Company


# permissions of models for roles
_models_roles_permissions = {
    **Company.get_permissions(),
}


class AccountManager(BaseUserManager):
    """Custom account model manager."""
    def create_user(self, username, email, password, **extra_fields):
        """Create and save a user with username, email, password."""
        self._check(username, email, password)

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with username, email, password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_valid", True)
        extra_fields.setdefault("is_blocked", False)
        extra_fields.setdefault("is_confirmed", True)
        extra_fields.setdefault("role", Account.Role.SU)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, email, password, **extra_fields)
    
    def _check(self, username, email, password) -> None:
        """Check username, email, password of account."""
        validators = {
            "username": is_username_valid(username),
            "email": is_email_valid(email),
            "password": is_password_valid(password)
        }
        validate_result, check_messages = True, []
        for key, validator in validators.items():
            check_result, fail_messages = validator
            if  check_result is False:
                validate_result = False
                check_messages.append(f"{key}:{fail_messages}")
        if validate_result is False:
            raise ValidationError(check_messages)


class AdminManager(AccountManager):
    """Custom account manager for role Admin."""
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.ADMIN)


class EmployeeManager(AccountManager):
    """Custom account manager for role Employee."""
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.EMPLOYEE)


class CustomerManager(AccountManager):
    """Custom account manager for role Customer"""
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.CUSTOMER)


class GuestManager(AccountManager):
    """Custom account manager for role Guest"""
    def get_queryset(self):
        return super().get_queryset().filter(role=Account.Role.GUEST)


class Account(TimestampsMixin, SoftDeleteMixin, RolePermissionsMixin, AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model."""

    class Role(models.TextChoices):
        SU = "SU", _("Superuser")
        ADMIN = "ADMIN", _("Admin")
        EMPLOYEE = "EMPLOYEE", _("Employee")
        CUSTOMER = "CUSTOMER", _("Customer")
        GUEST = "GUEST", _("Guest")

    username = models.CharField(
        max_length=settings.LENGTH["username"]["max"],
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=settings.LENGTH["email"]["max"],
        unique=True,
        validators=[validate_email]
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
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        verbose_name="Role",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = AccountManager.from_queryset(BaseQuerySet)()
    
    def __repr__(self) -> str:
        return self.username
    
    @property
    def confirmed(self) -> bool:
        return self.is_confirmed is True
    
    @confirmed.setter
    def confirmed(self, val: bool) -> None:
        self.is_confirmed = val
        self.actual = val
        self.save()
    
    @property
    def uid_token(self) -> tuple[str, str]:
        """Get uid and token of account."""
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = account_token.make_token(self)
        return uid, token

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]
        permissions = [
            ("view_dashboard", "View page: Dashboard"),
            ("change_password", "Change account password"),
            ("allow_chat", "Allow chat"),
        ]
    
    def save(self, set_permissions: bool = False, **kwargs):
        """Save or save with permissions by set_permissions."""
        super().save(**kwargs)
        if set_permissions:
            set_account_permissions(self, _models_roles_permissions)
    
    def delete(self, soft=False, **kwargs) -> None:
        """Delete or soft delete account."""
        if soft is True:
            self.is_active = False
            self.confirmed = False
        super().delete(soft=soft, **kwargs)
    
    @classmethod
    def get_by_uid(cls, uid: str) -> Self | None:
        """Get account by uid."""
        try:
            inst_id = force_str(urlsafe_base64_decode(uid))
            account = cls.objects.get(pk=inst_id)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            account = None

        return account
    
    def is_actual(self) -> Tuple[bool, List[str]]:
        """
        Get (tuple) is the model item actual (bool, 
        active and confirmed), with fail messages (list[str]).
        """
        is_actual, fail_messages = super().is_actual()
        if self.is_active is not None:
            is_actual = False
            fail_messages.append(_("Not active"))
        if self.is_confirmed is not None:
            is_actual = False
            fail_messages.append(_("Not confirmed"))
        
        return is_actual, fail_messages

    def check_token(self, token: str) -> bool:
        """Check account token"""
        return account_token.check_token(self, token)

    def check_password(self, pwd: str) -> bool:
        """Check account password"""
        return check_password(pwd, self.password)
    
    _permissions = {
        "account:account": {
            "admin": "__all__",
            "employee": [
                "view_dashboard",
                "change_password",
                "allow_chat",
                "change_profile",
            ],
            "customer": [
                "view_dashboard",
                "change_password",
                "allow_chat",
                "change_profile",
            ],
            "guest": [
                "allow_chat",
            ]
        },
    }

    @adm.display(description="Full name")
    def full_name(self):
        return self.profile.full_name

    @adm.display(description=_("Photo"))
    def photo_img(self):
        return self.profile.photo.get_html_img_tag(or_def_by_key="img_user", alt="img_user")


class Admin(Account):
    """Admin account"""
    objects = AdminManager.from_queryset(BaseQuerySet)()

    class Meta:
        proxy = True

    def save(self, *args, set_permissions: bool = False, **kwargs):
        """Save or save with permissions by set_permissions."""
        self.is_staff = True
        self.is_superuser = False
        self.role = Account.Role.ADMIN
        super().save(*args, **kwargs)
        if set_permissions:
            set_account_permissions(self, _models_roles_permissions)


class Employee(Account):
    """Employee account"""
    objects = EmployeeManager.from_queryset(BaseQuerySet)()

    class Meta:
        proxy = True

    def save(self, *args, set_permissions: bool = False, **kwargs):
        """Save or save with permissions by set_permissions."""
        self.is_staff = True
        self.is_superuser = False
        self.role = Account.Role.EMPLOYEE
        super().save(*args, **kwargs)
        if set_permissions:
            set_account_permissions(self, _models_roles_permissions)


class Customer(Account):
    """Customer account"""
    objects = CustomerManager.from_queryset(BaseQuerySet)()

    class Meta:
        proxy = True

    def save(self, *args, set_permissions: bool = False, **kwargs):
        """Save or save with permissions by set_permissions."""
        self.is_staff = False
        self.is_superuser = False
        self.role = Account.Role.CUSTOMER
        super().save(*args, **kwargs)
        if set_permissions:
            set_account_permissions(self, _models_roles_permissions)


class Guest(Account):
    """Guest account"""
    objects = GuestManager.from_queryset(BaseQuerySet)()

    class Meta:
        proxy = True

    def save(self, *args, set_permissions: bool = False, **kwargs):
        """Save or save with permissions by set_permissions."""
        self.is_staff = False
        self.is_superuser = False
        self.role = Account.Role.GUEST
        super().save(*args, **kwargs)
        if set_permissions:
            set_account_permissions(self, _models_roles_permissions)
