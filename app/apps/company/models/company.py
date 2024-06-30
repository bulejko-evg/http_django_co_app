from typing import Any
from django.db import models
from django.contrib import admin
from django.conf import settings
from app.vendors.base.model import BaseModel
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from app.vendors.helpers import remove_directory
from app.vendors.base.field import ExtImageField
from django.utils.translation import gettext_lazy as _
from django.db.models import (
    Prefetch,
    UniqueConstraint,
)
from app.vendors.helpers.validations import (
    validate_file_image,
    validate_file_icon,
)
from app.vendors.mixins.model import (
    NamesDescriptionsMixin,
    LanguageRichTextMixin,
    RolePermissionsMixin,
    TimestampsMixin,
    MetaDataMixin,
    CacheMixin,
)


def get_company_images_save_url(instance, filename):
    """Get url for save company images."""
    return f"{instance.get_instance_media_path()}/images/{filename}"


class Company(NamesDescriptionsMixin, TimestampsMixin, RolePermissionsMixin, CacheMixin, BaseModel):
    alias = models.CharField(
        max_length=settings.LENGTH["alias"]["max"],
        unique=True,
    )
    icon = ExtImageField(
        upload_to=get_company_images_save_url,
        null=True,
        blank=True,
        validators=[validate_file_icon],
    )
    logo = ExtImageField(
        upload_to=get_company_images_save_url,
        null=True,
        blank=True,
        validators=[validate_file_image],
    )
    banner = ExtImageField(
        upload_to=get_company_images_save_url,
        null=True,
        blank=True,
        validators=[validate_file_image],
    )
    settings = models.JSONField(
        default=dict,
    )

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        permissions = [
            ("change_settings", "Change company settings"),
        ]
        indexes = [
            models.Index(
                fields=["alias"]
            ),
        ]

    def __str__(self):
        return self.alias

    def __repr__(self):
        return f"{self.__class__.__name__}, alias: {self.alias}"

    @classmethod
    def cache_queryset(cls, **kwargs) -> Any:
        """Query set for CacheMixin"""
        _alias = kwargs.get("alias", settings.COMPANY_ALIAS)
        return cls.objects.actual().filter(alias=_alias).prefetch_related(
            Prefetch("trs", queryset=CompanyTranslate.objects.defer("rich_text"))
        ).first()

    def save(self, **kwargs):
        super().save(**kwargs)
        self.delete_cache(prefix=str(self.alias))

    def get_instance_media_path(self):
        """Get path for instance in settings.MEDIA_ROOT directory"""
        return f"{self.__class__.__name__.lower()}/{self.alias}/"

    _permissions = {
        "company:company": {
            "admin": [
                "view_company",
                "change_settings",
            ],
            "employee": [
                "view_company",
            ],
            "customer": [
                "view_company",
            ],
            "guest": [],
        }
    }

    @admin.display(description=_("Logo"))
    def logo_img(self):
        return self.logo.get_html_img_tag(or_def_by_key="logo", alt="img_logo")


@receiver(pre_delete, sender=Company)
def company_delete(sender, instance, **kwargs):
    # instance.icon.delete(False)
    # instance.logo.delete(False)
    # instance.banner.delete(False)
    media_dir = settings.MEDIA_ROOT / instance.get_instance_media_path()
    remove_directory(media_dir)


class CompanyTranslate(LanguageRichTextMixin, MetaDataMixin, models.Model):
    company = models.ForeignKey(
        "Company",
        related_name="trs",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Company translate")
        verbose_name_plural = _("Company translates")
        constraints = [
            UniqueConstraint(fields=["company_id", "lang"], name="company reach tex by lang")
        ]
