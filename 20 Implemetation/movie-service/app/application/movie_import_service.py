from app.infrastructure.in_memory_movie_provider import InMemoryExternalMovieProvider
from app.infrastructure.in_memory_movie_repository import InMemoryMovieRepository


class MovieImportService:
    def __init__(self, provider: InMemoryExternalMovieProvider, repository: InMemoryMovieRepository) -> None:
        self._provider = provider
        self._repository = repository

    async def import_movie_from_external_source(self, command: object) -> object:
        metadata = await self._provider.fetch_movie_metadata(command)
        exists = await self._repository.find_by_external_id(metadata["external_provider"], metadata["external_id"])
        if exists:
            return {"success": False, "reason": "duplicate", "movie": exists}
        movie_id = str(getattr(command, "movie_id", metadata["external_id"]))
        movie = {"movie_id": movie_id, **metadata, "active": True}
        await self._repository.create(movie)
        return {"success": True, "movie": movie}
