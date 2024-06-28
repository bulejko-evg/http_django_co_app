import re
from collections import UserList
from typing import (
    Tuple,
    List,
)


def check_full_match(
    pattern: re.Pattern | str,
    value: str,
    error_message: str,
    success_message: str = "",
) -> tuple[bool, str]:
    """
    Check value by re.fullmatch with pattern.
    -----------------------------------------
    Parameters:
        pattern (re.Pattern): re compile pattern
        value (str): value for checking
        error_message (str): error message
        success_message (str): success message, optional, default ""
    Returns:
        (tuple[bool, str]): result of checking, message
    """
    result_of_checking, message = True, success_message

    if re.fullmatch(pattern, value) is None:
        result_of_checking = False
        message = error_message

    return result_of_checking, message


class ChecksList(UserList):
    """
    List of checks, get result for validation
    Item for list is Callable object, must return tuple
    (result of checking, message)
    """
    def get_result(self, each: bool = False) -> Tuple[bool, List[str]] | List[Tuple[bool, str]]:
        """
        Get result of checks.
        ---------------------
        Parameters:
            each (bool): get list of checks
        Returns:
            (Tuple[bool, List[str]] | List[Tuple[bool, str]]): 
                result of checks (bool) and fail messages (list[str]), or list of tuples from each check
        """
        if each is True:
            list_of_checks = []
            for check in self:
                res, message = check
                list_of_checks.append((res, message))

            return list_of_checks

        result_of_checks, messages = True, []
        for check in self:
            check_result, message = check
            if check_result is False:
                result_of_checks = False
                messages.append(message)

        return result_of_checks, messages