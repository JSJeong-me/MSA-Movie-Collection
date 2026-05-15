from typing import Protocol


class MovieValidationPort(Protocol):
    async def verify_movie_exists_for_collection(self, query: object) -> object:
        ...
