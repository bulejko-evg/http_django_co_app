from typing import Any
from django.contrib import admin
from django.conf import settings
from django.db.models import Count
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from .filters import (
    LangsListFilter,
    ParentsFilter,
)
from app.vendors.helpers import (
    get_choices_of_languages,
    update_request_get_parameters,
)


class AdminLanguageChoiceMixin:
    """Admin language choice filter mixin"""
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        _langs = get_choices_of_languages(settings.LANGUAGES_CODES)
        if db_field.name == 'lang':
            kwargs['choices'] = _langs
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    langs_filter = [
        LangsListFilter,
    ]


class AdminParentMixin:
    """ Admin tree mixin """
    current_url_params = None

    def parent_queryset(self, query, request, order_by: str | None = "created_at"):
        """ Add in get_queryset method in AdminModel """
        self.current_url_params = request.GET

        _except = ["/change/", "/delete/"]
        if any([co for co in _except if co in request.path]):
            return query

        if not request.GET.get("parent"):
            query = query.filter(parent__isnull=True)
        query = query.annotate(num_child=Count("children"))
        if order_by:
            query = query.order_by(order_by)
        return query

    @admin.display(description="")
    def link_to_child(self, obj):
        _str_params = update_request_get_parameters(self.current_url_params, parent=obj.id)
        base_url = obj.get_admin_changelist_url()
        url = f"{base_url}{_str_params}"
        if obj.num_child:
            return format_html("<a href='%s'>&#9776;</a>" % url)
        else:
            return " "

    parents_filter = [
        ParentsFilter
    ]


class AdminTreeMixin(AdminParentMixin):
    """Admin tree mixin"""

    class Media:
        js = ["js/admin/tree.js"]


class AdminSoftDeleteChangeFormMixin:
    """Admin form mixin. Set keys and change response for soft delete"""
    @staticmethod
    def set_soft_delete_keys(obj: Any, extra_context: dict):
        """Set keys for soft delete"""
        if hasattr(obj, "soft_deleted"):
            extra_context["show_soft_delete"] = True
            if obj.soft_deleted:
                extra_context["soft_delete"] = True

    def soft_delete_response_change(self, request, obj):
        """Response change for soft delete"""
        if "_soft_delete_cancel" in request.POST:
            self.message_user(request, _("Unmark deleted"))
            obj.deleted = False
            if hasattr(obj, "actual"):
                obj.actual = True
            if hasattr(obj, "is_active"):
                obj.is_active = True
            obj.save()
            return HttpResponseRedirect(obj.get_admin_changelist_url())
        if "_soft_delete" in request.POST:
            self.message_user(request, _("Mark as deleted"))
            obj.deleted = True
            obj.save()
            return HttpResponseRedirect(obj.get_admin_changelist_url())
