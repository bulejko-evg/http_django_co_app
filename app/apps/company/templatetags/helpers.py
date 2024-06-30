from typing import Any
from django import template
from app.vendors import data
from django.conf import settings
from django.utils.translation import get_language
from app.vendors.helpers import (
    get_val_from_dict,
    get_file_url,
    get_dict_value_by_keychain,
)


register = template.Library()


@register.filter(name="in_lang")
def in_lang(val: dict, by_code: str | None = None) -> str:
    """Get value from json field, dict with key a language code, default in current language."""
    lang_code = by_code or get_language()
    return get_val_from_dict(val, lang_code)


@register.filter(name="url")
def url(file, default: str = settings.DEFAULT_IMAGE_KEY) -> str:
    """Get file url or default image by key from settings.DEFAULT_IMAGE_KEY."""
    return get_file_url(file, or_def_by_key=default)


@register.inclusion_tag("partials/form/field_errors.html")
def field_errors(errors, css_style: str = "", css_classes: str = ""):
    """Form field errors template."""
    return {"errors": errors, "css_style": css_style, "css_classes": css_classes}


@register.inclusion_tag("partials/languages.html")
def languages(lang_list: list[str] | None = None, current_lang: str | None = None):
    """Get languages lists, and current language."""
    list_of_languages = lang_list or settings.LANGUAGES_CODES
    lang_code = current_lang or get_language()
    langs = [lang for lang in data.LANGUAGES if lang.code in list_of_languages]
    return {"languages": langs, "current_lang": lang_code}


@register.inclusion_tag("partials/themes.html")
def themes(theme_list: list[str] = settings.THEMES):
    """Get themes, default settings.THEMES."""
    return {"themes": theme_list}


@register.inclusion_tag("partials/pagination.html")
def pagination(page_obj, href_url):
    """Pagination links. href_url is current url without ?page."""
    return {"page_obj": page_obj, "href_url": href_url}


@register.simple_tag
def settings_value(key) -> Any:
    """Get value from settings by key."""
    return getattr(settings, key, "")


@register.filter(name="company_settings")
def company_settings_value(company, keychain: str):
    """
    Get value from company.settings by keychain.
    ---------------------------------------------
    Parameters:
        company (Company): current page
        keychain (str): keychain, dot separator
    Returns:
        res (str): page settings value
    """
    res = ""
    if company:
        res = get_dict_value_by_keychain(company.settings, keychain)

    return res


@register.filter(name="to_range")
def to_range(value: int) -> range:
    """Get range from 1 to value."""
    value = value if value is not None else 0
    return range(1, int(value) + 1)


@register.filter(name="to_str")
def to_str(value) -> str:
    """Get value as str."""
    return str(value)


@register.filter(name="to_int")
def to_int(value) -> int:
    """Get value as int."""
    return int(value)
