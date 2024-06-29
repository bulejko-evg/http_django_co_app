from django.db import models
from django.conf import settings
from app.vendors.base.field import ExtImageField
from django.utils.translation import gettext_lazy as _
from app.vendors.helpers.validations import (
    validate_file_image,
    validate_user_age,
    validate_birthday,
    validate_username,
)


def get_profile_photo_save_url(instance, filename):
    """Get url for save profile photo image"""
    return f"account/{instance.account.username}/photo/{filename}"


class Profile(models.Model):
    """Profile for account"""
    class Gender(models.TextChoices):
        MALE = "MALE", _("Male")
        FEMALE = "FEMALE", _("Female")

    account = models.OneToOneField(
        "Account",
        on_delete=models.CASCADE,
        related_name="profile",
        primary_key=True,
    )
    _first_name = models.CharField(
        db_column="first_name",
        max_length=settings.LENGTH["name"]["max"],
        validators=[validate_username]
    )
    _middle_name = models.CharField(
        db_column="middle_name",
        max_length=settings.LENGTH["name"]["max"],
        null=True,
        blank=True,
        validators=[validate_username]
    )
    _last_name = models.CharField(
        db_column="last_name",
        max_length=settings.LENGTH["name"]["max"],
        validators=[validate_username]
    )
    photo = ExtImageField(
        upload_to=get_profile_photo_save_url,
        null=True,
        blank=True,
        validators=[validate_file_image],
    )
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[validate_user_age],
    )
    birthdate = models.DateField(
        null=True,
        blank=True,
        validators=[validate_birthday],
    )
    gender = models.CharField(
        max_length=8,
        choices=Gender.choices,
        default=Gender.MALE,
    )

    @property
    def first_name(self):
        return str(self._first_name).capitalize()

    @property
    def middle_name(self):
        return f" {str(self._middle_name).capitalize()}" if self._middle_name else " "

    @property
    def last_name(self):
        return str(self._last_name).capitalize()

    @property
    def full_name(self):
        """Get full name ('first_name middle_name last_name')"""
        return f"{self.first_name}{self.middle_name}{self.last_name}"

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
