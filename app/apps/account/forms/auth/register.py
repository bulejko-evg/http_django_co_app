from django import forms
from django.conf import settings
from app.vendors import messages as msg
from app.apps.account.models import Customer
from django.utils.translation import gettext_lazy as _
from app.vendors.helpers.validation import (
    is_username_valid,
    is_email_valid,
    is_password_valid,
)


class RegisterForm(forms.ModelForm):
    """Register account form"""
    first_name = forms.CharField(
        label=_("First name"),
        min_length=settings.LENGTH["name"]["min"],
        max_length=settings.LENGTH["name"]["max"],
        help_text=_("Required"),
    )
    middle_name = forms.CharField(
        label=_("Middle name"),
        min_length=settings.LENGTH["name"]["min"],
        max_length=settings.LENGTH["name"]["max"],
    )
    last_name = forms.CharField(
        label=_("Last name"),
        min_length=settings.LENGTH["name"]["min"],
        max_length=settings.LENGTH["name"]["max"],
        help_text=_("Required"),
    )
    username = forms.CharField(
        label=_("Username"),
        min_length=settings.LENGTH["username"]["min"],
        max_length=settings.LENGTH["username"]["max"],
        help_text=_("Required"),
        error_messages={
            "required": msg.REQUIRED
        }
    )
    email = forms.EmailField(
        label=_("Email"),
        min_length=settings.LENGTH["email"]["min"],
        max_length=settings.LENGTH["email"]["max"],
        help_text=_("Required"),
        error_messages={
            "required": msg.REQUIRED
        }
    )
    password = forms.CharField(
        label=_("Password"),
        min_length=settings.LENGTH["password"]["min"],
        max_length=settings.LENGTH["password"]["max"],
        help_text=_("Required"),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Repeat password"),
        min_length=settings.LENGTH["password"]["min"],
        max_length=settings.LENGTH["password"]["max"],
        help_text=_("Required"),
        widget=forms.PasswordInput
    )

    class Meta:
        model = Customer
        fields = ("username", "email",)
    
    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        is_valid, messages = is_username_valid(username)
        if not is_valid:
            forms.ValidationError(messages)
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        is_valid, messages = is_email_valid(email)
        if not is_valid:
            forms.ValidationError(messages)
        return email

    def clean_password2(self):
        passwd = self.cleaned_data.get("password")
        passwd2 = self.cleaned_data.get("password2")
        is_valid, messages = is_password_valid(passwd)
        if not is_valid:
            forms.ValidationError(messages)
        if passwd and passwd2 and passwd != passwd2:
            raise forms.ValidationError(msg.PASSWORD_MISMATCH)
        return passwd2
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

        self.fields["first_name"].widget.attrs.update(
            {"placeholder": _("First name")}
        )
        self.fields["middle_name"].widget.attrs.update(
            {"placeholder": _("Middle name")}
        )
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": _("Last name")}
        )
        self.fields["username"].widget.attrs.update(
            {"placeholder": _("Login")}
        )
        self.fields["email"].widget.attrs.update(
            {"type": "email", "placeholder": _("E-mail")}
        )
        self.fields["password"].widget.attrs.update(
            {"type": "password", "placeholder": _("Password")}
        )
        self.fields["password2"].widget.attrs.update(
            {"type": "password", "placeholder": _("Repeat password")}
        )
