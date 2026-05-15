class InMemoryMovieRepository:
    def __init__(self) -> None:
        self._movies: dict[str, dict] = {}

    async def create(self, movie: dict) -> dict:
        self._movies[movie["movie_id"]] = movie
        return movie

    async def update(self, movie_id: str, patch: dict) -> dict | None:
        item = self._movies.get(movie_id)
        if item is None:
            return None
        item.update(patch)
        return item

    async def get(self, movie_id: str) -> dict | None:
        return self._movies.get(movie_id)

    async def list_all(self) -> list[dict]:
        return [m for m in self._movies.values() if m.get("active", True)]

    async def find_by_external_id(self, provider: str, external_id: str) -> dict | None:
        for movie in self._movies.values():
            if movie.get("external_provider") == provider and movie.get("external_id") == external_id:
                return movie
        return None
