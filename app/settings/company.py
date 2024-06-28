from .settings import LANGUAGE_CODE

LANGUAGES_CODES = ["en", "ru"]
CURRENCIES_CODES = ["USD", "RUB"]
THEMES = ["light", "dark"]

COMPANY_ALIAS = "co"

COMPANY_SETTINGS = {
    "theme": "light",
    "layout": "layouts/top.html",
    "content_layout": "layouts/content/left.html",
    "language": LANGUAGE_CODE,
    "languages": LANGUAGES_CODES,
    "currencies": CURRENCIES_CODES,
    "themes": THEMES,
}