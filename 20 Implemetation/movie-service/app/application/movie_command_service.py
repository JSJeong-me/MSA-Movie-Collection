from app.events.movie_events import MovieEventPublisher
from app.infrastructure.in_memory_movie_repository import InMemoryMovieRepository


class MovieCommandService:
    def __init__(self, repository: InMemoryMovieRepository, event_publisher: MovieEventPublisher) -> None:
        self._repository = repository
        self._event_publisher = event_publisher

    async def create_movie(self, command: object) -> object:
        movie = {
            "movie_id": str(getattr(command, "movie_id", "")),
            "title": str(getattr(command, "title", "")),
            "description": str(getattr(command, "description", "")),
            "release_year": int(getattr(command, "release_year", 0)),
            "genres": list(getattr(command, "genres", [])),
            "cast": list(getattr(command, "cast", [])),
            "directors": list(getattr(command, "directors", [])),
            "active": True,
        }
        if not movie["movie_id"] or not movie["title"]:
            return {"success": False, "reason": "movie_id and title are required"}
        await self._repository.create(movie)
        await self._event_publisher.publish_movie_created_event(movie)
        return {"success": True, "movie": movie}

    async def update_movie(self, command: object) -> object:
        movie_id = str(getattr(command, "movie_id", ""))
        patch = dict(getattr(command, "patch", {}))
        updated = await self._repository.update(movie_id, patch)
        if updated is None:
            return {"success": False, "reason": "movie not found"}
        await self._event_publisher.publish_movie_updated_event(updated)
        return {"success": True, "movie": updated}

    async def deactivate_movie(self, command: object) -> object:
        movie_id = str(getattr(command, "movie_id", ""))
        updated = await self._repository.update(movie_id, {"active": False})
        if updated is None:
            return {"success": False, "reason": "movie not found"}
        await self._event_publisher.publish_movie_deleted_event({"movie_id": movie_id})
        return {"success": True, "movie_id": movie_id}

    async def update_movie_cast(self, command: object) -> object:
        movie_id = str(getattr(command, "movie_id", ""))
        cast = list(getattr(command, "cast", []))
        directors = list(getattr(command, "directors", []))
        updated = await self._repository.update(movie_id, {"cast": cast, "directors": directors})
        if updated is None:
            return {"success": False, "reason": "movie not found"}
        await self._event_publisher.publish_movie_updated_event(updated)
        return {"success": True, "movie": updated}
