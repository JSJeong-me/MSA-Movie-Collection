from typing import Protocol


class ExternalMovieProviderPort(Protocol):
    async def fetch_movie_metadata(self, query: object) -> object:
        ...
