from django.utils.translation import gettext_lazy as _


WHITESPACE_MESSAGE = _("Spaces are not allowed")
INVALID_LENGTH_MESSAGE = _("Length is not valid (min %(min)s, max %(max)s).")
MUST_BE_SET_MESSAGE = _("The %(name)s must be set")
INVALID_CHARACTER_SET_MESSAGE = _("Is not valid character(s), allowed (%(from_set)s)")
AT_LEAST_ONE_MESSAGE = _("Must be at least one %(from_set)s")
TOO_BIG_MESSAGE = _("Too big. (max %(max)s)")
TOO_SMALL_MESSAGE = _("Too small. (min %(min)s)")
INVALID_FILE = _("Invalid file %(details)s")
INVALID_SVG_HTML_MESSAGE = _("Invalid SVG")
INVALID_LANGUAGE_CODE = _("Invalid language code")

W_DOT_DASH_SET = _("Letters, numbers or symbols .-_")
W_DOT_DASH_SPACE_SET = _("Letters, numbers or symbols .-_ and space")
EMAIL_SET = _(
    "For name valid (Letters, numbers or symbols .-_),"
    "for domain valid, before dot (Letters, numbers)"
    "after dot (Letters, numbers or symbols .-)"
)
URL_SET = _("Must start with http:// or https://, and any non-whitespace characters")
LETTERS_UPPER_SET = _("from A to Z")
LETTERS_LOWER_SET = _("from a to z")
NUMBERS_SET = _("from 0 to 9")

PASSWORD_MISMATCH = _("Passwords do not match")
REQUIRED = _("Required field")
MODEL_ITEM_EXIST = _("A %(model)s with this %(field)s already exists")
