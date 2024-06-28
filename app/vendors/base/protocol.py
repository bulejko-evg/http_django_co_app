from typing import Protocol


class FileProtocol(Protocol):

    @property
    def url(self) -> str:
        """Get file url"""
        ...

    @property
    def path(self) -> str:
        """Get file path"""
        ...

    def get_extension(self) -> str:
        """Get file extension"""
        ...

    def is_empty(self) -> bool:
        """Get file is empty"""
        ...