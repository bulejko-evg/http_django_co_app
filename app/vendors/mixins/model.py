from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from typing import (
    Any,
    Tuple,
    List,
)


class TimestampsMixin(models.Model):
    """
    A date and time of creation and update mixin.
    ---------------------------------------------
    Attributes:
        created_at (models.DateTimeField): a date and time of creation
        updated_at (models.DateTimeField): a date and time of updation
    """
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    A date and time of soft deletion mixin.
    ---------------------------------------
    Attributes:
        deleted_at (models.DateTimeField): a date and time of deletion
    Properties:
        deleted: get (bool) the deleted_at is None
    Methods:
        delete (soft=False): delete or soft delete 
        is_actual (): get tuple, is the model item actual (deleted_at is None), with fail messages (list[str])
    """
    deleted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    @property
    def deleted(self) -> bool:
        """Get the deleted_at is None."""
        return self.deleted_at is not None
    
    @deleted.setter
    def deleted(self, val: bool) -> None:
        """Set deleted_at as timezone.now or None."""
        self.deleted_at = timezone.now() if val is True else None

    class Meta:
        abstract = True
    
    def delete(self, soft=False, **kwargs) -> None:
        """Delete or soft delete."""
        if soft is True:
            self.deleted_at = timezone.now()
        super().delete(soft=soft, **kwargs)
    
    def is_actual(self) -> Tuple[bool, List[str]]:
        """
        Get (tuple) is the model item actual (bool, deleted_at is None), 
        with fail messages (list[str])."""
        is_actual, fail_messages = super().is_actual()
        if self.deleted_at is not None:
            is_actual = False
            fail_messages.append(_("Deleted"))
        
        return is_actual, fail_messages


class RolePermissionsMixin(models.Model):
    """
    Permissions for model by roles.
    --------------------------------
    Attributes:
        _permissions (dict): {<app name:mode name>:{<role name>:[list os permissions] or "__all__"str}}
    Methods:
        get_permissions (): get attribute _permissions or empty dict
        __set
    """
    # dict permissions for roles: {<app name:mode name>:{<role name>:[list os permissions] or "__all__"str}}
    _permissions = {}

    class Meta:
        abstract = True
    
    def get_permissions(self) -> dict:
        """Get _permissions attribute or empty dict."""
        return getattr(self, "_permissions", {})
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Prohibit attribute _permissions changes."""
        if name == "_permissions":
            return
        return super().__setattr__(name, value)
