from shared.contracts.event_envelope import EventEnvelope

from app.infrastructure.in_memory_search_index_repository import InMemorySearchIndexRepository


class SearchIndexEventHandler:
    def __init__(self, repository: InMemorySearchIndexRepository) -> None:
        self._repository = repository

    async def handle_movie_created(self, event: object) -> object:
        payload = getattr(event, "payload", {})
        movie_id = str(payload.get("movie_id", ""))
        await self._repository.upsert(movie_id, {**payload, "search_doc_status": "active"})
        return {"updated": True, "movie_id": movie_id}

    async def handle_movie_updated(self, event: object) -> object:
        payload = getattr(event, "payload", {})
        movie_id = str(payload.get("movie_id", ""))
        existing = await self._repository.get(movie_id) or {}
        existing.update(payload)
        await self._repository.upsert(movie_id, existing)
        return {"updated": True, "movie_id": movie_id}

    async def handle_movie_deleted(self, event: object) -> object:
        payload = getattr(event, "payload", {})
        movie_id = str(payload.get("movie_id", ""))
        await self._repository.delete(movie_id)
        return {"updated": True, "movie_id": movie_id}

    async def handle_review_created(self, event: object) -> object:
        _ = event
        return {"updated": True}

    async def handle_review_deleted(self, event: object) -> object:
        _ = event
        return {"updated": True}

    async def handle_rating_updated(self, event: object) -> object:
        payload = getattr(event, "payload", {})
        movie_id = str(payload.get("movie_id", ""))
        doc = await self._repository.get(movie_id) or {"movie_id": movie_id}
        doc["average_rating"] = payload.get("average_rating", payload.get("score", 0))
        await self._repository.upsert(movie_id, doc)
        return {"updated": True, "movie_id": movie_id}

    async def rebuild_movie_search_document(self, command: object) -> object:
        movie_id = str(getattr(command, "movie_id", ""))
        doc = await self._repository.get(movie_id)
        return {"movie_id": movie_id, "document": doc}


async def subscribe_search_handlers(handler: SearchIndexEventHandler, subscribe: callable) -> None:
    async def _created(event: EventEnvelope[object]) -> None:
        await handler.handle_movie_created(event)

    async def _updated(event: EventEnvelope[object]) -> None:
        await handler.handle_movie_updated(event)

    async def _deleted(event: EventEnvelope[object]) -> None:
        await handler.handle_movie_deleted(event)

    subscribe("MovieCreated", _created)
    subscribe("MovieUpdated", _updated)
    subscribe("MovieDeleted", _deleted)
