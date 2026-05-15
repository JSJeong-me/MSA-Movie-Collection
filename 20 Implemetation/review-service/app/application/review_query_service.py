class ReviewQueryService:
    def __init__(self, review_repository: object, rating_repository: object) -> None:
        self._review_repository = review_repository
        self._rating_repository = rating_repository

    async def get_reviews_by_movie(self, query: object) -> object:
        return {"items": await self._review_repository.list_by_movie(str(getattr(query, "movie_id", "")))}

    async def get_my_reviews(self, query: object) -> object:
        return {"items": await self._review_repository.list_by_user(str(getattr(query, "user_id", "")))}

    async def get_review_detail(self, query: object) -> object:
        return {"review": await self._review_repository.get(str(getattr(query, "review_id", "")))}

    async def get_rating_summary_by_movie(self, query: object) -> object:
        return await self._rating_repository.summary(str(getattr(query, "movie_id", "")))

    async def get_my_rating_for_movie(self, query: object) -> object:
        score = await self._rating_repository.get(str(getattr(query, "user_id", "")), str(getattr(query, "movie_id", "")))
        return {"score": score}

    async def check_review_ownership(self, query: object) -> object:
        review = await self._review_repository.get(str(getattr(query, "review_id", "")))
        return {"owned": bool(review and review.get("user_id") == str(getattr(query, "user_id", "")))}
