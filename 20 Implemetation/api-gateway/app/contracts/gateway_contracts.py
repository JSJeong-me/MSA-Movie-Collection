from dataclasses import dataclass


@dataclass(frozen=True)
class ProxyRequest:
    method: str
    path: str
    headers: dict[str, str]
    body: bytes | None


@dataclass(frozen=True)
class ProxyResponse:
    status_code: int
    data: dict
