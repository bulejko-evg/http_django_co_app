from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from app.vendors.mixins.view import (
    ContextDataMixin,
    LoginPermissionRequiredMixin,
)


class BaseView(ContextDataMixin, View):
    pass


class BaseListView(ContextDataMixin, ListView):
    pass


class BaseTemplateView(ContextDataMixin, TemplateView):
    pass


class BaseDetailView(ContextDataMixin, DetailView):
    pass


class BaseFormView(ContextDataMixin, FormView):
    pass


class ProtectBaseView(ContextDataMixin, LoginPermissionRequiredMixin, View):
    pass


class ProtectBaseListView(ContextDataMixin, LoginPermissionRequiredMixin, ListView):
    pass


class ProtectBaseTemplateView(ContextDataMixin, LoginPermissionRequiredMixin, TemplateView):
    pass


class ProtectBaseDetailView(ContextDataMixin, LoginPermissionRequiredMixin, DetailView):
    pass


class ProtectBaseFormView(ContextDataMixin, LoginPermissionRequiredMixin, FormView):
    pass
