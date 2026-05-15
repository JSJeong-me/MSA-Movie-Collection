from types import SimpleNamespace

from app.ports.movie_validation_port import MovieValidationPort


class InMemoryMovieValidationAdapter(MovieValidationPort):
    def __init__(self, checker: callable) -> None:
        self._checker = checker

    async def verify_movie_exists_for_collection(self, query: object) -> object:
        movie_id = str(getattr(query, "movie_id", ""))
        return await self._checker(SimpleNamespace(movie_id=movie_id))
