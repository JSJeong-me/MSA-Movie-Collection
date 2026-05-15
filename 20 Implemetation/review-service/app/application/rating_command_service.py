class RatingCommandService:
    def __init__(self, rating_repository: object, movie_validation_port: object, event_publisher: object) -> None:
        self._rating_repository = rating_repository
        self._movie_validation_port = movie_validation_port
        self._event_publisher = event_publisher

    async def create_or_update_rating(self, command: object) -> object:
        exists = await self._movie_validation_port.verify_movie_exists_for_review(command)
        if not exists.get("exists", False):
            return {"success": False, "reason": "movie not found"}
        score = max(1, min(5, int(getattr(command, "score", 0))))
        user_id = str(getattr(command, "user_id", ""))
        movie_id = str(getattr(command, "movie_id", ""))
        await self._rating_repository.upsert(user_id, movie_id, score)
        summary = await self._rating_repository.summary(movie_id)
        await self._event_publisher.publish_rating_updated_event({"movie_id": movie_id, "average_rating": summary["average"], "count": summary["count"]})
        return {"success": True, "score": score, "summary": summary}

    async def delete_rating(self, command: object) -> object:
        removed = await self._rating_repository.delete(str(getattr(command, "user_id", "")), str(getattr(command, "movie_id", "")))
        return {"success": removed}
