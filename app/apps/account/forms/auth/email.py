from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from app.vendors.helpers.validation import is_email_valid


class GetEmailForm(PasswordResetForm):
	"""Email form"""
	email = forms.EmailField(
		label=_("Email"),
		max_length=settings.LENGTH["email"]["max"],
		help_text=_("Required"),
		widget=forms.TextInput(
			attrs={
				"type": "email",
				"id": "form-email",
				"class": "form-control",
				"placeholder": _("Email"),
			}
		)
	)

	def clean_email(self):
		email = self.cleaned_data["email"]
		is_valid, messages = is_email_valid(email)
		if not is_valid:
			forms.ValidationError(messages)
		return email
