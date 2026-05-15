from shared.contracts.event_envelope import EventEnvelope
from shared.infrastructure.runtime import event_bus


class InMemoryEventPublisher:
    async def publish_event(self, event: EventEnvelope[object]) -> None:
        await event_bus.publish(event)
