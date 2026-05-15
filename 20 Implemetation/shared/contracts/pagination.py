from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    """Pagination request contract."""

    page: int
    size: int
