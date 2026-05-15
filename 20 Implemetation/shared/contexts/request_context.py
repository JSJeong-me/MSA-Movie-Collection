from dataclasses import dataclass


@dataclass(frozen=True)
class RequestContext:
    """
    Describes the request-level execution context shared across services.
    """

    request_id: str
    correlation_id: str | None = None
