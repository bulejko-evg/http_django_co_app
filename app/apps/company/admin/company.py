from django.contrib import admin
from django.conf import settings
from app.vendors.base.model.admin import AdminBaseModel
from app.vendors.mixins.admin import AdminLanguageChoiceMixin
from app.apps.company.forms.admin.company import (
    CompanyForm,
    CompanyTranslateForm,
)
from app.apps.company.models import (
    Company,
    CompanyTranslate,
)


@admin.register(Company)
class CompanyAdmin(AdminBaseModel):
    form = CompanyForm

    def get_queryset(self, request):
        return super().get_queryset(request)

    list_display = (
        "alias",
        *Company.names_display,
        "logo_img",
        *Company.actual_display,
        "created_at",
    )
    list_filter = (*Company.actual_filters,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "alias",
                    *Company.names_descriptions_fieldsets,
                )
            },
        ),
        (
            "Validation",
            {
                "fields": (*Company.actual_fieldsets,),
            },
        ),
        (
            "Images",
            {
                "fields": (
                    "icon",
                    "logo",
                    "banner",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": ("settings",),
            },
        ),
    )
    search_fields = ("alias",)
    prepopulated_fields = {
        "alias": ("names",),
    }

    def save_model(self, request, obj, form, change) -> None:
        super().save_model(request, obj, form, change)
        obj.icon.resize(width=settings.IMAGE_WIDTH["icon"])
        obj.logo.resize(width=settings.IMAGE_WIDTH["logo"])

    actions = [
        *Company.actual_actions,
    ]


@admin.register(CompanyTranslate)
class CompanyTranslateAdmin(AdminLanguageChoiceMixin, AdminBaseModel):
    form = CompanyTranslateForm

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("company")

    list_display = (
        "company",
        "lang",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "company",
                    *CompanyTranslate.language_rich_text_fieldsets,
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (*CompanyTranslate.meta_data_fieldsets,),
            },
        ),
    )
    search_fields = ("company__slug",)
    raw_id_fields = [
        "company",
    ]
