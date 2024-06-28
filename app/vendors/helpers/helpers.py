import string
import secrets
from app.vendors import data
from datetime import datetime
from django.conf import settings
from collections import UserDict
from django.templatetags.static import static
from django.utils.crypto import get_random_string
from app.vendors.base.protocol import FileProtocol
from django.utils.html import (
    format_html,
    format_html_join,
)
from random import (
    shuffle,
    choice,
)
from app.vendors.exceptions import (
    GetFileUrlError,
    GetFilePathError,
)
from typing import (
    List, 
    Tuple, 
    Any,
)


def get_val_from_dict(dict_: dict | UserDict, by_key: str, or_dafault: Any | None = None) -> Any:
    """Get value from dict by key or default value"""
    return dict_.get(by_key, or_dafault)


def get_file_url(file: FileProtocol, or_def_by_key: str | None = None) -> str:
    """
    Get a file url, or url of default file by or_def_by_key from settings.DEFAULT_FILES,
    if or_def_by_key is None and file url not exist, raise exception GetFileUrlError.
    -----------------------------------------------------------------------------------
    Parameters:
        file (FileProtocol): field file
        or_def_by_key: (str | None): key of default file path, optional, default None
    Returns:
        (str): get file url, or url of default file by or_def_by_key from settings.DEFAULT_FILES
    Raise:
        GetFileUrlError: if or_def_by_key is None and file.url raise Exception
    """
    try:
        url = file.url
    except Exception as exc:
        if or_def_by_key is None:
            raise GetFileUrlError from exc
        url = static(settings.DEFAULT_FILES[or_def_by_key])
    
    return url


def get_file_path(file: FileProtocol, or_def_by_key: str | None = None) -> str:
    """
    Get a file path, or url of default file by or_def_by_key from settings.DEFAULT_FILES,
    if or_def_by_key is None and file url not exist, raise exception GetFileUrlError.
    -----------------------------------------------------------------------------------
    Parameters:
        file (FileProtocol): field file
        or_def_by_key: (str | None): key of default file path, optional, default None
    Returns:
        (str): get file path, or url of default file by or_def_by_key from settings.DEFAULT_FILES
    Raise:
        GetFileUrlError: if or_def_by_key is None and file.url raise Exception
    """
    try:
        path = file.path
    except Exception as exc:
        if or_def_by_key is None:
            raise GetFilePathError from exc
        path = static(settings.DEFAULT_FILES[or_def_by_key])
    
    return path


def get_html_tag_attributes(**kwargs: str) -> str:
    """
    Get attributes for html tag from kwargs.
    -----------------------------------------
    Parameters:
        **kwargs (str): attributes for html tag
    Returns:
        (str): format html str
    """
    return format_html_join(
        sep=" ",
        format_string="{}={}",
        args_generator=((k, v) for k, v in kwargs.items())
    )


def get_html_tag_style(**kwargs: str) -> str:
    """
    Get style for html tag from kwargs.
    Parameters:
        **kwargs (str): style values for html tag
    Returns:
        (str): format html str
    """
    return format_html_join(
        sep=";",
        format_string="{}:{}",
        args_generator=((k, v) for k, v in kwargs.items())
    )


def get_format_html_img(src: str, width: int, **attributes: str) -> str:
    """
    Get format html img tag by src, width and any attributes.
    ---------------------------------------------------------
    Parameters:
        src (str): image src
        width (int): image width
        **attributes (str): tags for html image tag
    Returns:
        (str): format html image tag
    """
    attrs_str = get_html_tag_attributes(**attributes)
    return format_html(f"<img width='{width}' src='{src}' {attrs_str}/>")


def get_file_extensions_by_key(by_key: str, file_types: dict | None = None) -> List[str]:
    """
    Get file extensions by file type.
    ---------------------------------
    Parameters:
        by_key (str): file type key
        file_types (dict): file types
    Returns:
        res (list[str]): extensions for file type
    """
    res = []
    types = file_types or settings.FILE_TYPES
    for ft in types.get(by_key, []):
        ext = ft[0] if isinstance(ft, tuple) else ft
        res.append(str(ext))
    return res


def get_choices_of_languages(
        langs_codes: list[str] | None = None,
        languages: list[data.Language] | None = None
    ) -> List[Tuple[int, int]]:
    """
    Get languages choices list.
    ---------------------------
    Parameters:
        langs_codes (str): file type key
        languages: (list[data.Language]): list of namedtuple Language(name, code)
    Returns:
        langs_choices list[tuple[str, str]]: tuple language name, language code
    """
    codes = langs_codes or settings.LANGUAGES_CODES
    data_languages = languages or data.LANGUAGES
    langs_choices = [(lang.code, lang.name,) for lang in data_languages if lang.code in codes]
    return langs_choices


def generate_password(
        qty: int = settings.PASSWORD_LENGTH,
        characters: tuple[str] = settings.CHARACTERS_FOR_PASSWORD
    ) -> str:
    """
    Generate a password from a tuple of strings in the quantity.
    ------------------------------------------------------------
    Parameters:
        qty (int): quantity of characters in the password
        characters (tuple[str]): tuple of character resource strings
    Returns:
        password (str): string of random characters
    """
    password_characters = []

    for i in range(qty):
        # one character from each source str
        # others from a random source str
        from_character_str = characters[i] if i < len(characters) else choice(characters)
        random_character = secrets.choice(from_character_str)  # get random character
        password_characters.append(random_character)

    shuffle(password_characters)  # mix characters
    password = "".join(password_characters)
    return password


def get_unique_str(by_len: int = 15) -> str:
    """
    Get unique str by length.
    -------------------------
    Parameters:
        by_len (int): length for result str
    Returns:
        (str): unique str
    """
    return get_random_string(by_len, allowed_chars=string.ascii_uppercase + string.digits)


def get_unique_int() -> int:
    """
    Get unique int by timestamp.
    ----------------------------
    Returns:
        (str): unique int
    """
    return int(datetime.now().timestamp())


def get_dict_value_by_keychain(dict_: dict, keychain: str) -> Any:
    """
    Get value from dict by keychain (str with dot separator).
    ---------------------------------------------------------
    Parameters:
        src (dict): data dict
        keychain (str): keychain, dot separator
    Returns:
        res (Any): value from dict, or None
    """
    res = dict_
    list_of_keys = keychain.split(".")

    for key in list_of_keys:
        try:
            res = res.get(key, None)
        except AttributeError:
            res = None
            break
        if res is None: #  value by key not exist
            break

    return res
