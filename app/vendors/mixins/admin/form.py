from .filters import SoftDeleteFilter
from .admin import AdminSoftDeleteChangeFormMixin


class AdminChangeFormMixin(AdminSoftDeleteChangeFormMixin):
    """Admin change form mixin"""
    change_form_template = "admin/change_form.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context if extra_context is not None else {}
        obj = self.get_queryset(request).get(pk=object_id)
        self.set_soft_delete_keys(obj, extra_context)
        return self.changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        self.soft_delete_response_change(request, obj)
        return super().response_change(request, obj)

    soft_delete_filter = [
        SoftDeleteFilter,
    ]
