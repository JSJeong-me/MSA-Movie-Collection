from app.application.search_index_event_handler import SearchIndexEventHandler
from app.application.search_query_service import SearchQueryService
from app.infrastructure.in_memory_search_index_repository import InMemorySearchIndexRepository
from shared.infrastructure.runtime import event_bus

search_repository = InMemorySearchIndexRepository()
search_query_service = SearchQueryService(search_repository)
search_index_event_handler = SearchIndexEventHandler(search_repository)


async def _movie_created(event: object) -> None:
    await search_index_event_handler.handle_movie_created(event)


async def _movie_updated(event: object) -> None:
    await search_index_event_handler.handle_movie_updated(event)


async def _movie_deleted(event: object) -> None:
    await search_index_event_handler.handle_movie_deleted(event)


event_bus.subscribe("MovieCreated", _movie_created)
event_bus.subscribe("MovieUpdated", _movie_updated)
event_bus.subscribe("MovieDeleted", _movie_deleted)
