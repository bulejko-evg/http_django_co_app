from django.conf import settings
from django.urls import reverse_lazy
from app.vendors.base.context import ContexData
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from typing import (
    Any,
    Callable,
)

_context: ContexData[str, Callable] = ContexData({})


class ContextDataMixin(ContextMixin):
    """
    Get common data mixin
    Attributes:
        company (Any | dict | None): company data
    Methods:
        get_context_data: get dict of context with common data from apps
    """
    company: Any | None = None  # company instance, default company dict from settings or None

    def get_context_data(self, **kwargs):
        """Get common context data"""
        kwargs["request_path"] = self.request.path
        context = super().get_context_data(**kwargs)
        context = {**context, **_context.get_data(**kwargs)}
        self.company = context.get("company", None)
        return context


class LoginPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Login and permission required mixin
    Methods:
        get_login_url: get login url
    """
    def get_login_url(self):
        """Get login url"""
        return reverse_lazy(settings.LOGIN_URL)
