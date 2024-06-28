from django.conf import settings
from django.template import loader
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from app.vendors.helpers import get_html_tag_attributes


class JsonFieldDictTabsWidget(TextInput):
    """Tabs for JsonField with dict"""

    def __init__(self, **kwargs):
        self.attrs = kwargs.get("attrs", None)
        self.items = settings.LANGUAGES_CODES
        self.def_item = settings.LANGUAGE_CODE
        super().__init__(attrs=self.attrs)

    def get_context(self, name, value, attrs=None):
        attrs = get_html_tag_attributes(**{**self.attrs, **attrs})
        tab_items = self.items
        tab_item = self.def_item
        return {
            "widget": {
                "name": name,
                "value": value,
                "tab_items": tab_items,
                "attrs": attrs,
                "def_item": tab_item,
            }
        }

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

    class Media:
        js = ["js/widget/json_tabs.js"]


class NamesTabsWidget(JsonFieldDictTabsWidget):
    """Names JsonField Tabs widget"""
    template_name = "src/widget/names_tabs.html"


class DescriptionsTabsWidget(JsonFieldDictTabsWidget):
    """Descriptions JsonField Tabs widget"""
    template_name = "src/widget/descriptions_tabs.html"

