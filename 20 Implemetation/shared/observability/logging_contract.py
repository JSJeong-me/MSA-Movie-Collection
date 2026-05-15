from abc import ABC, abstractmethod


class LoggingContract(ABC):
    """Simple logging abstraction for app services."""

    @abstractmethod
    def info(self, message: str, **kwargs: object) -> None:
        ...

    @abstractmethod
    def error(self, message: str, **kwargs: object) -> None:
        ...
