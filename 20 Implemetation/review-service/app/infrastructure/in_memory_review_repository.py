class InMemoryReviewRepository:
    def __init__(self) -> None:
        self._reviews: dict[str, dict] = {}

    async def create(self, review: dict) -> dict:
        self._reviews[review["review_id"]] = review
        return review

    async def get(self, review_id: str) -> dict | None:
        return self._reviews.get(review_id)

    async def list_by_movie(self, movie_id: str) -> list[dict]:
        return [r for r in self._reviews.values() if r.get("movie_id") == movie_id and not r.get("hidden", False)]

    async def list_by_user(self, user_id: str) -> list[dict]:
        return [r for r in self._reviews.values() if r.get("user_id") == user_id]

    async def update(self, review_id: str, patch: dict) -> dict | None:
        r = self._reviews.get(review_id)
        if not r:
            return None
        r.update(patch)
        return r
