import re
import magic
import string
import datetime
from functools import partial
from django.conf import settings
from collections import defaultdict
from app.vendors import messages as msg
from app.vendors.base.protocol import FileProtocol
from app.vendors.base.check import check_full_match
from app.vendors.helpers import get_file_extensions_by_key
from typing import (
    Tuple,
    List,
)


len_username = settings.LENGTH["username"]
len_email = settings.LENGTH["email"]
len_password = settings.LENGTH['password']


whitespace_pattern = re.compile(r"^\S*$")
w_dot_dash_pattern = re.compile(r"^[\w.-]+$")
w_dot_dash_space_pattern = re.compile(r"^[\w. -]+$")
at_least_one_punctuation_pattern = re.compile(r"^.*[!\"#\$%&\\'()*+,-./:;<=>?@\[\]\^_`{|}~]+.*$")
at_least_one_lowercase_pattern = re.compile(r"^.*[a-z]+.*$")
at_least_one_uppercase_pattern = re.compile(r"^.*[A-Z]+.*$")
at_least_one_number_pattern = re.compile(r"^.*[0-9]+.*$")
email_pattern = re.compile(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$")
url_pattern = re.compile(r"^[(http|https)]+:\/\/(www.)?[\S]+$")
length_str_pattern = r"\S{%s,%s}"


check_whitespace = partial(
    check_full_match,
    pattern=whitespace_pattern,
    error_message=msg.WHITESPACE_MESSAGE
)
check_w_dot_dash = partial(
    check_full_match,
    pattern=w_dot_dash_pattern,
    error_message=msg.INVALID_CHARACTER_SET_MESSAGE % {"from_set": msg.W_DOT_DASH_SET}
)
check_w_dot_dash_space = partial(
    check_full_match,
    pattern=w_dot_dash_space_pattern,
    error_message=msg.INVALID_CHARACTER_SET_MESSAGE % {"from_set": msg.W_DOT_DASH_SPACE_SET}
)
check_email = partial(
    check_full_match,
    pattern=email_pattern,
    error_message=msg.INVALID_CHARACTER_SET_MESSAGE % {"from_set": msg.EMAIL_SET}
)
check_url = partial(
    check_full_match,
    pattern=url_pattern,
    error_message=msg.INVALID_CHARACTER_SET_MESSAGE % {"from_set": msg.URL_SET}
)
check_at_least_one_punctuation = partial(
    check_full_match,
    pattern=at_least_one_punctuation_pattern,
    error_message=msg.AT_LEAST_ONE_MESSAGE % {"from_set": string.punctuation}
)
check_at_least_one_lowercase = partial(
    check_full_match,
    pattern=at_least_one_lowercase_pattern,
    error_message=msg.AT_LEAST_ONE_MESSAGE % {"from_set": msg.LETTERS_LOWER_SET}
)
check_at_least_one_uppercase = partial(
    check_full_match,
    pattern=at_least_one_uppercase_pattern,
    error_message=msg.AT_LEAST_ONE_MESSAGE % {"from_set": msg.LETTERS_UPPER_SET}
)
check_at_least_one_number = partial(
    check_full_match,
    pattern=at_least_one_number_pattern,
    error_message=msg.AT_LEAST_ONE_MESSAGE % {"from_set": msg.NUMBERS_SET}
)


def check_length(
        value: str, 
        min_length: int, 
        max_length: int, 
        success_message: str | None = None
    ) -> Tuple[bool, str]:
    """
    Check length.
    -------------
    Parameters:
        value (str): value for checking
        min_length (int): min length
        max_length (int): max length
        success_message (str): success message, optional, default None
    Returns:
        (Tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message
    if not min_length < len(value) < max_length:
        result_of_checking = False
        message = msg.INVALID_LENGTH_MESSAGE % {"min": min_length, "max": max_length}

    return result_of_checking, message


def check_file_size(
        file: FileProtocol, 
        by_file_type_key: str, 
        success_message: str | None = None
    ) -> Tuple[bool, str]:
    """
    Check file size.
    ----------------
    Parameters:
        file (FieldFile): file for checking
        by_file_type_key (str): key type of files from settings.FILE_TYPES
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message
    max_size = settings.FILE_SIZES[by_file_type_key]
    if not file.is_empty() and file.size > max_size:
        result_of_checking = False
        message = msg.TOO_BIG_MESSAGE % {"max": max_size}

    return result_of_checking, message


def check_file_extension(
        file: FileProtocol, 
        by_file_type_key: str, 
        success_message: str | None = None
    ) -> Tuple[bool, str]:
    """
    Check file extension.
    ---------------------
    Parameters:
        file (FieldFile): file for checking
        by_file_type_key (str): key type of files from settings.FILE_TYPES
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message

    type_extensions = get_file_extensions_by_key(by_file_type_key)

    if not file.is_empty() and file.extension not in type_extensions:
        result_of_checking = False
        message = msg.INVALID_FILE % {
            "details": f"type (valid types {type_extensions})"
        }

    return result_of_checking, message


def check_file_mime_buff(
        file: FileProtocol, 
        by_file_type_key: str, 
        success_message: str | None = None
    ) -> Tuple[bool, str]:
    """
    Check file mime or buffer.
    --------------------------
    Parameters:
        file (FieldFile): file for checking
        by_file_type_key (str): key type of files from settings.FILE_TYPES
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message
    if not file._file:
        return result_of_checking, message

    file_type = settings.FILE_TYPES[by_file_type_key]

    ext_mime_buff_dict = {}
    for ft in file_type:
        if isinstance(ft, tuple):
            ext, mime, buff = ft
        else:
            ext, mime, buff = ft, None, None
        ext_mime_buff_dict[ext] = mime, buff

    ext_mime_buff = ext_mime_buff_dict.get(file.extension, None)
    if ext_mime_buff is not None and any(ext_mime_buff):
        mime, buff = ext_mime_buff[0], ext_mime_buff[1]
        if mime is not None:
            initial_pos = file.tell()
            file.seek(0)
            file_type_mime = magic.from_buffer(file.read(settings.FILE_BYTE_TO_CHECK), mime=True)
            file.seek(initial_pos)
            if not file_type_mime == mime:
                result_of_checking = False
                message = msg.INVALID_FILE % {"details": "fail MIME"}
        if buff is not None:
            initial_pos = file.tell()
            file.seek(0)
            file_type_buff = magic.from_buffer(file.read(settings.FILE_BYTE_TO_CHECK))
            file.seek(initial_pos)
            if buff not in file_type_buff:
                result_of_checking = False
                message = msg.INVALID_FILE % {"details": "fail BUFFER"}

    return result_of_checking, message


def check_svg_html(svg: str, success_message: str | None = None) -> Tuple[bool, str]:
    """
    Check svg str.
    --------------
    Parameters:
        svg (str): svg html str for checking
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message
    conditions = [
        svg.startswith("<svg"),
        svg.endswith("</svg>"),
        "script" not in svg,
        svg.count("<") - svg.count(">") == 0
    ]
    if not all(conditions):
        result_of_checking = False
        message = msg.INVALID_SVG_HTML_MESSAGE

    return result_of_checking, message


def check_user_age(age: int, success_message: str | None = None) -> Tuple[bool, str]:
    """
    Check age
    Parameters:
        age (int): age for checking
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message

    if age < settings.USER_AGE["min"]:
        result_of_checking = False
        message = msg.TOO_SMALL_MESSAGE % {"min": settings.USER_AGE["min"]}
    if age > settings.USER_AGE["max"]:
        result_of_checking = False
        message = msg.TOO_BIG_MESSAGE % {"max": settings.USER_AGE["max"]}

    return result_of_checking, message


def check_birthday(date: datetime.date, success_message: str | None = None) -> tuple[bool, str]:
    """
    Check birthday.
    ---------------
    Parameters:
        date (str | date): date
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message
    min_birthdate = date - datetime.timedelta(days=settings.BIRTHDAY_TIMEDELTA_YEARS * 364)
    max_birthdate = datetime.date.today()

    if date < min_birthdate:
        result_of_checking = False
        message = msg.TOO_SMALL_MESSAGE % {"min": min_birthdate}
    if date > max_birthdate:
        result_of_checking = False
        message = msg.TOO_BIG_MESSAGE % {"max": max_birthdate}

    return result_of_checking, message


def check_language_codes(codes: List[str], success_message: str | None = None) -> Tuple[bool, str]:
    """
    Check codes of languages.
    -------------------------- 
    Parameters:
        codes: (list[str]): list of languages codes
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages
    """
    result_of_checking, message = True, success_message
    if not set(codes).issubset(set(settings.LANGUAGES_CODES)):
        result_of_checking = False
        message = msg.INVALID_LANGUAGE_CODE

    return result_of_checking, message


def check_json_names(names: dict, success_message: str | None = None) -> Tuple[bool, str]:
    """
    Check names.
    ------------
    Parameters:
        names: (list): names for checking
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages (str)
    """
    result_of_checking, message = True, success_message
    name_length = settings.LENGTH["name"]
    _messages = defaultdict(list)

    for lang_code, name in names.items():
        if not name_length["min"] < len(name) < name_length["max"]:
            result_of_checking = False
            _messages[lang_code].append(
                msg.INVALID_LENGTH_MESSAGE % {"min": name_length["min"], "max": name_length["max"]}
            )
        
        is_valid, message = check_w_dot_dash_space(value=name)
        if not is_valid:
            _messages[lang_code].append(message)
    
    message = ";".join([f"{k}:{','.join(v)}" for k, v in _messages.items()])

    return result_of_checking, message


def check_json_descriptions(descriptions: dict, success_message: str | None = None) -> tuple[bool, str]:
    """
    Check descriptions.
    -------------------
    Parameters:
        descriptions: (list): description for checking
        success_message (str): success message, optional, default None
    Returns:
        (tuple[bool, str]): result of checking, messages (str)
    """
    result_of_checking, message = True, success_message
    description_length = settings.LENGTH["description"]
    _messages = defaultdict(list)

    for lang_code, description in descriptions.items():
        if not description_length["min"] < len(description) < description_length["max"]:
            result_of_checking = False
            _messages[lang_code].append(
                msg.INVALID_LENGTH_MESSAGE % {"min": description_length["min"], "max": description_length["max"]}
            )
    
    message = ";".join([f"{k}:{','.join(v)}" for k, v in _messages.items()])

    return result_of_checking, message