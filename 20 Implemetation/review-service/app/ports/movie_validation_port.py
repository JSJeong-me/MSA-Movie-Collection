from typing import Protocol


class MovieValidationPort(Protocol):
    async def verify_movie_exists_for_review(self, query: object) -> object:
        ...
