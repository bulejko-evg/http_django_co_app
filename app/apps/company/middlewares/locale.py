from django.utils.translation import get_language
from django.utils import translation


def set_language_middleware(get_response):
    """Set current language, by value current_lang from session"""
    def middleware(request):
        if current_lang := request.session.get('current_lang', False):
            lang = current_lang
        else:
            lang = get_language()
        translation.activate(lang)
        response = get_response(request)
        translation.deactivate()
        return response

    return middleware