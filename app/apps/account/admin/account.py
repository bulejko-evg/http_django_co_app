from typing import Any
from django.contrib import admin
from django.conf import settings
from django.db import transaction
from django.http.request import HttpRequest
from django.contrib.auth.admin import UserAdmin
from app.vendors.base.model.admin import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from app.apps.account.forms.admin import (
    AccountCreationForm,
    AccountChangeForm,
    ProfileForm,
)
from app.apps.account.models import (
    Account,
    Profile,
)


class ProfileInline(admin.StackedInline):
    form = ProfileForm
    model = Profile
    max_num = 1
    extra = 1
    can_delete = False
    verbose_name_plural = _("Profile")
    fk_name = "account"


@admin.register(Account)
class AccountAdmin(UserAdmin, AdminBaseModel):
    add_form = AccountCreationForm
    form = AccountChangeForm

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")

    list_display = (
        "username",
        "photo",
        "email",
        "full_name",
        "is_staff",
        "is_active",
        *Account.actual_display,
        "created_at",
    )
    list_filter = (
        *Account.actual_filters,
        "is_staff",
        "role",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        (
            "Validation",
            {
                "fields": (
                    "is_active",
                    *Account.actual_fieldsets,
                    "is_staff",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Validation",
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    *Account.actual_fieldsets,
                    "is_staff",
                    "role",
                ),
            },
        ),
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = [
        "-created_at",
    ]
    list_select_related = [
        "profile",
    ]
    inlines = [
        ProfileInline,
    ]

    def save_model(self, request, obj, form, change) -> None:
        super().save_model(request, obj, form, change)

    def save_formset(self, request: Any, form: Any, formset: Any, change: Any) -> None:
        super().save_formset(request, form, formset, change)
        for f in formset.forms:
            obj = f.instance
            obj.save()
            obj.photo.resize(width=settings.IMAGE_WIDTH["user"])

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        obj.profile.photo.delete()
        return super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        with transaction.atomic():
            for obj in queryset:
                obj.profile.photo.delete()
                obj.delete()

    actions = [
        *Account.actual_actions,
        *Account.soft_deleted_actions,
    ]
