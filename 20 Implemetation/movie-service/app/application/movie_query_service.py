from app.infrastructure.in_memory_movie_repository import InMemoryMovieRepository


class MovieQueryService:
    def __init__(self, repository: InMemoryMovieRepository) -> None:
        self._repository = repository

    async def get_movie_list(self, query: object) -> object:
        _ = query
        return {"items": await self._repository.list_all()}

    async def get_movie_detail(self, query: object) -> object:
        movie_id = str(getattr(query, "movie_id", ""))
        movie = await self._repository.get(movie_id)
        return {"movie": movie}

    async def check_movie_exists(self, query: object) -> object:
        movie_id = str(getattr(query, "movie_id", ""))
        movie = await self._repository.get(movie_id)
        return {"exists": movie is not None and movie.get("active", False)}

    async def get_movie_summary(self, query: object) -> object:
        movie_id = str(getattr(query, "movie_id", ""))
        movie = await self._repository.get(movie_id)
        if not movie:
            return {"movie": None}
        return {"movie": {"movie_id": movie_id, "title": movie.get("title"), "release_year": movie.get("release_year")}}

    async def find_movie_by_external_id(self, query: object) -> object:
        provider = str(getattr(query, "provider", ""))
        external_id = str(getattr(query, "external_id", ""))
        movie = await self._repository.find_by_external_id(provider, external_id)
        return {"movie": movie}
