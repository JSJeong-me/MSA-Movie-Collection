from typing import Protocol

from shared.contracts.event_envelope import EventEnvelope


class EventPublisherPort(Protocol):
    async def publish_event(self, event: EventEnvelope[object]) -> None:
        ...
