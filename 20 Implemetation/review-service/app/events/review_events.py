from datetime import datetime, timezone
from uuid import uuid4

from shared.contracts.event_envelope import EventEnvelope
from shared.ports.event_publisher_port import EventPublisherPort


class ReviewEventPublisher:
    def __init__(self, event_publisher: EventPublisherPort) -> None:
        self._event_publisher = event_publisher

    async def publish_review_created_event(self, payload: object) -> None:
        await self._event_publisher.publish_event(EventEnvelope(str(uuid4()), "ReviewCreated", datetime.now(timezone.utc), "review-service", payload))

    async def publish_review_deleted_event(self, payload: object) -> None:
        await self._event_publisher.publish_event(EventEnvelope(str(uuid4()), "ReviewDeleted", datetime.now(timezone.utc), "review-service", payload))

    async def publish_rating_updated_event(self, payload: object) -> None:
        await self._event_publisher.publish_event(EventEnvelope(str(uuid4()), "RatingUpdated", datetime.now(timezone.utc), "review-service", payload))
