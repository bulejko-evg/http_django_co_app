import datetime
from functools import partial
from django.conf import settings
from app.vendors.base.check import ChecksList
from django.core.exceptions import ValidationError
from app.vendors.base.protocol import FileProtocol
from .checks import (
    check_whitespace,
    check_length,
    check_w_dot_dash,
    check_w_dot_dash_space,
    check_email,
    check_url,
    check_at_least_one_punctuation,
    check_at_least_one_lowercase,
    check_at_least_one_uppercase,
    check_at_least_one_number,
    check_file_size,
    check_file_extension,
    check_file_mime_buff,
    check_user_age,
    check_birthday,
    check_svg_html,
    check_language_codes,
    check_json_names,
    check_json_descriptions,
)
from typing import (
    Tuple,
    List,
)


len_username = settings.LENGTH["username"]
len_email = settings.LENGTH["email"]
len_url = settings.LENGTH["url"]
len_password = settings.LENGTH["password"]
len_comment = settings.LENGTH["comment"]


def is_username_valid(value: str) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check username.
    ----------------
    Parameters:
        value (str): username
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_whitespace(value=value),
        check_length(value=value, min_length=len_username["min"], max_length=len_username["max"]),
        check_w_dot_dash(value=value),
    ])
    return checks.get_result()


def is_email_valid(value: str) ->  Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check email.
    ------------
    Parameters:
        value (str): email
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_whitespace(value=value),
        check_length(value=value, min_length=len_email["min"], max_length=len_email["max"]),
        check_email(value=value),
    ])
    return checks.get_result()


def is_password_valid(value: str) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check password.
    ---------------
    Parameters:
        value (str): password
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_whitespace(value=value),
        check_length(value=value, min_length=len_password["min"], max_length=len_password["max"]),
        check_at_least_one_number(value=value),
        check_at_least_one_lowercase(value=value),
        check_at_least_one_uppercase(value=value),
        check_at_least_one_punctuation(value=value)
    ])
    return checks.get_result()


def is_url_valid(value: str) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check url.
    -----------
    Parameters:
        value (str): url
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_whitespace(value=value),
        check_length(value=value, min_length=len_url["min"], max_length=len_url["max"]),
        check_url(value=value),
    ])
    return checks.get_result()


def is_user_age_valid(age: int) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check user age
    Parameters:
        age (int): age for checking
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_user_age(age=age),
    ])
    return checks.get_result()


def is_svg_html_valid(svg: str) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check html svg str.
    -------------------
    Parameters:
        svg (str): svg html str for checking
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_svg_html(svg=svg),
    ])
    return checks.get_result()


def is_birthday_valid(date: datetime.date) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check birthday.
    ---------------
    Parameters:
        date (str): date for checking
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_birthday(date=date)
    ])
    return checks.get_result()


def is_json_names_valid(names: dict) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check json names.
    -----------------
    Parameters:
        names (dict): names dict from json field
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_language_codes(codes=list(names.keys())),
        check_json_names(names=names),
    ])

    return checks.get_result()


def is_json_descriptions_valid(descriptions: dict) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check json descriptions.
    ------------------------
    Parameters:
        descriptions (dict): descriptions dict from json field
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_language_codes(codes=list(descriptions.keys())),
        check_json_descriptions(descriptions=descriptions)
    ])

    return checks.get_result()


def is_comment_valid(value: str) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check comment.
    --------------
    Parameters:
        value (str): comment
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_length(value=value, min_length=len_comment["min"], max_length=len_comment["max"]),
        check_w_dot_dash_space(value=value),
    ])
    return checks.get_result()


def is_file_valid(
        file: FileProtocol,
        by_file_type_key: str,
        strict: bool = settings.FILE_STRICT_CHECKING
    ) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
    """
    Check file size, file extension and file mime, file buffer if strict is True.
    ------------------------------------------------------------------------------
    Parameters:
        file (FieldFile): file for check
        strict (bool): flag for strict checking of file (mime, buffer)
        by_file_type_key (str): key type of files from settings.FILE_TYPES
    Returns:
        (Tuple[bool, List[str]] | List[Tuple[bool, str]]):
            result of checks (bool) and fail messages (list[str]), or list of tuples from each check
    """
    checks = ChecksList([
        check_file_size(file=file, by_file_type_key=by_file_type_key),
        check_file_extension(file=file, by_file_type_key=by_file_type_key),
    ])
    if strict:
        checks.append(
            check_file_mime_buff(file=file, by_file_type_key=by_file_type_key)
        )

    return checks.get_result()


def validate_username(val: str) -> None:
    """Validate username"""
    is_valid, messages = is_username_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_password(val: str) -> None:
    """Validate password"""
    is_valid, messages = is_password_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_email(val: str) -> None:
    """Validate email"""
    is_valid, messages = is_email_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_url(val: str) -> None:
    """Validate url"""
    is_valid, messages = is_url_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_user_age(val: int) -> None:
    """Validate user age"""
    is_valid, messages = is_user_age_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_birthday(val: datetime.date) -> None:
    """Validate user birthday"""
    is_valid, messages = is_birthday_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_json_names(value: dict) -> None:
    """Validate json names"""
    is_valid, messages = is_json_names_valid(value)
    if not is_valid:
        raise ValidationError(messages)


def validate_json_descriptions(value: dict) -> None:
    """Validate json descriptions"""
    is_valid, messages = is_json_descriptions_valid(value)
    if not is_valid:
        raise ValidationError(messages)


def validate_comment(val: str) -> None:
    """Validate comment"""
    is_valid, messages = is_comment_valid(val)
    if not is_valid:
        raise ValidationError(messages)


def validate_svg_html(value: str) -> None:
    """Validate svg html str"""
    is_valid, messages = is_svg_html_valid(value)
    if not is_valid:
        raise ValidationError(messages)


def validate_file(val: FileProtocol, file_type_key: str) -> None:
    """Validate file by file type"""
    is_valid, messages = is_file_valid(val, file_type_key)
    if not is_valid:
        raise ValidationError(messages)


validate_file_image = partial(validate_file, file_type_key="image")
validate_file_thumb = partial(validate_file, file_type_key="thumb")
validate_file_icon = partial(validate_file, file_type_key="icon")
validate_file_video = partial(validate_file, file_type_key="video")
validate_file_audio = partial(validate_file, file_type_key="audio")
validate_file_doc = partial(validate_file, file_type_key="doc")