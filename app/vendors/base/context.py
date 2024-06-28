from typing import Callable
from collections import UserDict


class ContexData(UserDict):
    """
    Get data for view get_contex_data
    self is: dict[str, Callable]
    """

    def __init__(self, data: dict[str, Callable]):
        super().__init__(data)

    def get_data(self, **kwargs) -> dict:
        """Get data updated with data from kwargs"""
        result_ctx_data = {key: get_ctx_data(**kwargs) for key, get_ctx_data in self.items()}

        return result_ctx_data


