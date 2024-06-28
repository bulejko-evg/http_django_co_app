import string
import secrets
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
    pass
