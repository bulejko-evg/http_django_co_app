from django import forms
from app.apps.account.models import Profile


class ProfileForm(forms.ModelForm):
    """Admin form for profile"""

    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "gender": forms.RadioSelect,
        }
