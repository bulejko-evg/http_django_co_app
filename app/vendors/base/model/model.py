from django.db import models
from django.contrib import admin
from django.conf import settings
from .queryset import BaseQuerySet
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from typing import (
    Tuple,
    List,
)


@admin.action(description=_("Mark selected as valid"))
def make_valid(modeladmin, request, queryset):
    """Mark as valid"""
    queryset.update(is_valid=True)


@admin.action(description=_("Mark selected as not valid"))
def make_invalid(modeladmin, request, queryset):
    """Mark as invalid"""
    queryset.update(is_valid=False)


@admin.action(description=_("Mark selected as blocked"))
def make_blocked(modeladmin, request, queryset):
    """Mark as blocked"""
    queryset.update(is_blocked=True)


@admin.action(description=_("Mark selected as unblocked"))
def make_unblocked(modeladmin, request, queryset):
    """Mark as unblocked"""
    queryset.update(is_blocked=False)


class BaseModel(models.Model):
    """
    Base class for models.
    ----------------------
    Attributes:
        is_valid (models.BooleanField): the item model is valid (for admin)
        is_blocked (models.BooleanField): the item is blocked (for superuser only)
    Properties:
        actual (): get and set (bool), is_valid and not is_blocked
    Methods:
        delete (soft=False): delete or soft delete
        is_actual (): get tuple, is the model item actual (valid and not blocked), with fail messages (list[str])
    Admin:
        blocked: svg icon for admin table
        actual_list_display: actual fields list_display
        actual_list_filter: actual fields list_filter
        actual_fieldsets: actual fields
        actual_actions: model actual actions
    """
    is_valid = models.BooleanField(
        default=False
    )
    is_blocked = models.BooleanField(
        default=True
    )

    objects = BaseQuerySet.as_manager()

    @property
    def actual(self) -> bool:
        return self.is_valid and not self.is_blocked
    
    @actual.setter
    def actual(self, val) -> None:
        self.is_valid = val
        self.is_blocked = not val

    class Meta:
        verbose_name = None
        abstract = True
    
    def delete(self, soft=False, **kwargs) -> None:
        """Delete or soft delete"""
        if soft is True:
            self.is_valid = False
            self.is_blocked = True
            self.save()
            return
        super().delete(**kwargs)
    
    def is_actual(self) -> Tuple[bool, List[str]]:
        """Get (tuple) is the model item actual (bool, valid and not blocked), with fail messages (list[str])"""
        is_actual, fail_messages = True, []
        if self.is_valid is False:
            is_actual = False
            fail_messages.append(_("Not valid"))
        if self.is_blocked is True:
            is_actual = False
            fail_messages.append(_("Blocked"))
        
        return is_actual, fail_messages
    
    @admin.display(description=_("Blocked"))
    def blocked(self):
        """Get blocked svg icon or None."""
        if self.is_blocked:
            return format_html(settings.SVG["block"])
        return None
    
    actual_display = (
        "is_valid",
        "blocked",
    )
    actual_filters = (
        "is_blocked",
        "is_valid",
    )
    actual_fieldsets = (
        "is_blocked",
        "is_valid",
    )
    actual_actions = [
        make_valid,
        make_invalid,
        make_blocked,
        make_unblocked,
    ]
