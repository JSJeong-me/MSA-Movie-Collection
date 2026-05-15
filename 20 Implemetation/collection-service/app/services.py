from app.application.collection_command_service import CollectionCommandService
from app.application.collection_query_service import CollectionQueryService
from app.infrastructure.in_memory_collection_repository import InMemoryCollectionRepository
from app.infrastructure.in_memory_movie_validation_adapter import InMemoryMovieValidationAdapter


async def _stub_movie_check(query: object) -> object:
    return {"exists": bool(getattr(query, "movie_id", ""))}


collection_repository = InMemoryCollectionRepository()
collection_command_service = CollectionCommandService(collection_repository, InMemoryMovieValidationAdapter(_stub_movie_check))
collection_query_service = CollectionQueryService(collection_repository)
