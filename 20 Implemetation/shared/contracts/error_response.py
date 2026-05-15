from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorResponse:
    """Standard API error payload."""

    code: str
    message: str
    details: dict | None = None
