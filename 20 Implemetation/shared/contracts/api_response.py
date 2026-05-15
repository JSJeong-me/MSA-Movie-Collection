from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ApiResponse:
    """Standard API response wrapper."""

    success: bool
    data: Any
    message: str | None = None
