import logging
from typing import Literal
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.core.cache import cache
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
    Page,
)


app_logger = logging.getLogger("app")
type CacheQuerysetKey = Literal["queryset", "get", "first"]


class BaseQuerySet(models.QuerySet):
    """Base queryset for models"""

    def blocked(self, blocked: bool = True):
        """Filter by field is_blocked, with value blocked (bool)"""
        return self.filter(is_blocked=blocked)

    def valid(self, valid: bool = True):
        """Filter by field is_valid, with value valid (bool)"""
        return self.filter(is_valid=valid)

    def actual(self, actual: bool = True):
        """Filter by fields is_blocked and is_valid, with value actual (bool)"""
        return self.filter(is_blocked=not actual, is_valid=actual)

    def created(self, account):
        """Filter by field created, with value account (Account)"""
        return self.filter(created=account)

    def updated(self, account):
        """Filter by field updated, with value account (Account)"""
        return self.filter(updated=account)

    def deleted(self, deleted: bool = True):
        """Filter by field deleted_at, with value deleted (bool)"""
        return self.filter(deleted_at__isnull=not deleted)

    def or_cache(
        self,
        by_key,
        queryset_as: CacheQuerysetKey = "queryset",
        timeout: int = settings.CACHE_TIME_DEFAULT,
        **get_kwargs: any,
    ):
        """
        Get result of quryset from cache or set cache if not exist.
        -----------------------------------------------------------
        Parameters:
            by_key (str): cache key
            queryset_as (CacheQuerysetKey): Literal ("queryset", "get", "first")
                key for queryset
            timeout (int): cache timeout
            **get_kwargs: parameters for get queryset
        Returns:
            cache value or queryset
        """
        res = cache.get(by_key, None)
        if res is None:
            match queryset_as:
                case "get":
                    res = self.get(**get_kwargs)
                case "first":
                    res = self.first()
                case "queryset":
                    res = self
            cache.set(by_key, res, timeout=timeout)
        return res

    def pagination(self, page: int = 1, per_page: int = settings.NUMBER_PER_PAGE) -> Page:
        """
        Get pagination objects from queryset.
        -------------------------------------
        Parameters:
            page (int): start page, optional, default 1
            per_page (int): number per page, optional, default settings.NUMBER_PER_PAGE
        Returns:
            page_obj (Page): paginator.Page object
        """
        paginator = Paginator(self, per_page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # first page
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # last page
        return page_obj