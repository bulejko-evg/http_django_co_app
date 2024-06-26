from django.db import models
from .queryset import BaseQuerySet
from django.utils.translation import gettext_lazy as _
from typing import (
    Tuple,
    List,
)


class BaseModel(models.Model):
    """
    Base class for models.
    ----------------------
    Attributes:
        is_valid (models.BooleanField): the item model is valid (for admin)
        is_blocked (models.BooleanField): the item is blocked (for superuser only) 
    Methods:
        delete (soft=False): delete or soft delete
        is_actual (): get tuple, is the model item actual (valid and not blocked), with fail messages (list[str])
    """
    is_valid = models.BooleanField(
        default=False
    )
    is_blocked = models.BooleanField(
        default=True
    )

    objects = BaseQuerySet.as_manager()

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