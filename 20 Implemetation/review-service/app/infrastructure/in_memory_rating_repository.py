class InMemoryRatingRepository:
    def __init__(self) -> None:
        self._ratings: dict[tuple[str, str], int] = {}

    async def upsert(self, user_id: str, movie_id: str, score: int) -> None:
        self._ratings[(user_id, movie_id)] = score

    async def delete(self, user_id: str, movie_id: str) -> bool:
        return self._ratings.pop((user_id, movie_id), None) is not None

    async def get(self, user_id: str, movie_id: str) -> int | None:
        return self._ratings.get((user_id, movie_id))

    async def summary(self, movie_id: str) -> dict:
        scores = [s for (u, m), s in self._ratings.items() if m == movie_id]
        if not scores:
            return {"count": 0, "average": 0.0}
        return {"count": len(scores), "average": sum(scores) / len(scores)}
