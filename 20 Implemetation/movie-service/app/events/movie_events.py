from datetime import datetime, timezone
from uuid import uuid4

from shared.contracts.event_envelope import EventEnvelope
from shared.ports.event_publisher_port import EventPublisherPort


class MovieEventPublisher:
    def __init__(self, event_publisher: EventPublisherPort) -> None:
        self._event_publisher = event_publisher

    async def publish_movie_created_event(self, payload: object) -> None:
        event = EventEnvelope(event_id=str(uuid4()), event_type="MovieCreated", occurred_at=datetime.now(timezone.utc), source="movie-service", payload=payload)
        await self._event_publisher.publish_event(event)

    async def publish_movie_updated_event(self, payload: object) -> None:
        event = EventEnvelope(event_id=str(uuid4()), event_type="MovieUpdated", occurred_at=datetime.now(timezone.utc), source="movie-service", payload=payload)
        await self._event_publisher.publish_event(event)

    async def publish_movie_deleted_event(self, payload: object) -> None:
        event = EventEnvelope(event_id=str(uuid4()), event_type="MovieDeleted", occurred_at=datetime.now(timezone.utc), source="movie-service", payload=payload)
        await self._event_publisher.publish_event(event)
