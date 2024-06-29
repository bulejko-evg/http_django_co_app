from django import forms
from django.conf import settings
from app.vendors import messages as msg
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from app.vendors.helpers.validation import is_password_valid


class ChangePasswdForm(SetPasswordForm):
	"""Change password form"""
	new_password1 = forms.CharField(
		label=_("New password"),
		min_length=settings.LENGTH["password"]["min"],
		max_length=settings.LENGTH["password"]["max"],
		help_text=_("Required"),
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"id": "newpass",
				"class": "form-control",
				"placeholder": _("New Password"),
			}
		))
	new_password2 = forms.CharField(
		label=_("Repeat password"),
		min_length=settings.LENGTH["password"]["min"],
		max_length=settings.LENGTH["password"]["max"],
		help_text=_("Required"),
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"id": "newpass2",
				"class": "form-control",
				"placeholder": _("New Password"),
			}
		))

	def clean_new_password2(self):
		new_passwd1 = self.cleaned_data["new_password1"]
		new_passwd2 = self.cleaned_data["new_password2"]
		is_valid, messages = is_password_valid(new_passwd1)
		if not is_valid:
			forms.ValidationError(messages)
		if new_passwd1 != new_passwd2:
			raise forms.ValidationError(msg.PASSWORD_MISMATCH)
		return new_passwd1
