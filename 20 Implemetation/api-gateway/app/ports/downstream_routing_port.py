from abc import ABC, abstractmethod


class DownstreamRoutingPort(ABC):
    """Forwards validated requests to target service."""

    @abstractmethod
    async def forward(self, method: str, path: str, headers: dict, body: bytes | None) -> dict:
        ...
