from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from app.vendors.helpers.validation import (
    is_username_valid,
    is_password_valid,
)


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(
        label=_("Username"),
        min_length=settings.LENGTH["username"]["min"],
        max_length=settings.LENGTH["username"]["max"],
        help_text=_("Required"),
    )
    password = forms.CharField(
        label=_("Password"),
        min_length=settings.LENGTH["password"]["min"],
        max_length=settings.LENGTH["password"]["max"],
        help_text=_("Required"),
        widget=forms.PasswordInput(),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        is_valid, messages = is_username_valid(username)
        if not is_valid:
            forms.ValidationError(messages)
        return username
    
    def clean_password(self):
        passwd = self.cleaned_data["password"]
        is_valid, messages = is_password_valid(passwd)
        if not is_valid:
            forms.ValidationError(messages)
        return passwd
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs.update({"placeholder": _("username")})
        self.fields["password"].widget.attrs.update({"placeholder": _("password")})
