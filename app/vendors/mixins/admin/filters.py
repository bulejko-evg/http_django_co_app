from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from app.vendors.helpers import get_choices_of_languages


class SoftDeleteFilter(admin.SimpleListFilter):
    """Admin SimpleListFilter, for deleted_at (soft deleted) field filter"""
    title = _("Soft deleted")

    parameter_name = "deleted_at"

    def lookups(self, request, model_admin):
        return [
            ("soft_deleted",     _("Yes")),
            ("not_soft_deleted", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "soft_deleted":
            return queryset.filter(deleted_at__isnull=False)
        if self.value() == "not_soft_deleted":
            return queryset.filter(deleted_at__isnull=True)


class LangsListFilter(admin.SimpleListFilter):
    """Admin SimpleListFilter, for lang field filter"""
    title = _("Languages")

    parameter_name = "lang"

    def lookups(self, request, model_admin):
        return get_choices_of_languages(settings.LANGUAGES_CODES)

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(lang=self.value())


class ParentsFilter(admin.SimpleListFilter):
    """Admin SimpleListFilter, for parent field filter"""
    title = _("Parents")

    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string(remove=[self.parameter_name]),
            "display": _("Top"),
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }

    parameter_name = "parent"

    def lookups(self, request, model_admin):
        parent_id = request.GET.get("parent", None)
        parent = model_admin.model.objects.filter(pk=parent_id).first()
        _items = []
        if parent:
            for p in parent.parents:
                _items.append((str(p.id), str(p)))
        return _items

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(parent_id=self.value())