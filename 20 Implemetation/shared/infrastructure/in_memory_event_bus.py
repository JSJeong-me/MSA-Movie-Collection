from collections import defaultdict
from collections.abc import Awaitable, Callable

from shared.contracts.event_envelope import EventEnvelope


Handler = Callable[[EventEnvelope[object]], Awaitable[None]]


class InMemoryEventBus:
    """Simple async pub/sub bus for local skeleton integration flows."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: EventEnvelope[object]) -> None:
        for handler in self._handlers.get(event.event_type, []):
            await handler(event)
