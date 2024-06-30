from django import forms
from django.conf import settings
from app.vendors.mixins.form import (
    NamesDescriptionsTabsByLangMixin, 
    RichTextMixin,
)
from app.apps.company.models import (
    Company,
    CompanyTranslate,
)


class CompanyForm(NamesDescriptionsTabsByLangMixin, forms.ModelForm):
    """Admin form for company."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["settings"].initial = settings.COMPANY_SETTINGS

    class Meta(NamesDescriptionsTabsByLangMixin.Meta):
        model = Company
        fields = "__all__"


class CompanyTranslateForm(RichTextMixin, forms.ModelForm):
    """Admin form for company translate."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rich_text"].required = False
    
    class Meta(RichTextMixin.Meta):
        model = CompanyTranslate
        fields = "__all__"

