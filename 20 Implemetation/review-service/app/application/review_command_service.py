class ReviewCommandService:
    def __init__(self, review_repository: object, movie_validation_port: object, event_publisher: object) -> None:
        self._review_repository = review_repository
        self._movie_validation_port = movie_validation_port
        self._event_publisher = event_publisher

    async def create_review(self, command: object) -> object:
        exists = await self._movie_validation_port.verify_movie_exists_for_review(command)
        if not exists.get("exists", False):
            return {"success": False, "reason": "movie not found"}
        review = {
            "review_id": str(getattr(command, "review_id", "")),
            "movie_id": str(getattr(command, "movie_id", "")),
            "user_id": str(getattr(command, "user_id", "")),
            "content": str(getattr(command, "content", "")),
            "hidden": False,
        }
        await self._review_repository.create(review)
        await self._event_publisher.publish_review_created_event(review)
        return {"success": True, "review": review}

    async def update_review(self, command: object) -> object:
        updated = await self._review_repository.update(str(getattr(command, "review_id", "")), {"content": str(getattr(command, "content", ""))})
        return {"success": updated is not None, "review": updated}

    async def delete_review(self, command: object) -> object:
        review_id = str(getattr(command, "review_id", ""))
        updated = await self._review_repository.update(review_id, {"hidden": True})
        if updated:
            await self._event_publisher.publish_review_deleted_event({"review_id": review_id, "movie_id": updated.get("movie_id")})
        return {"success": updated is not None}

    async def hide_review_by_admin(self, command: object) -> object:
        updated = await self._review_repository.update(str(getattr(command, "review_id", "")), {"hidden": True, "moderated": True})
        return {"success": updated is not None, "review": updated}
