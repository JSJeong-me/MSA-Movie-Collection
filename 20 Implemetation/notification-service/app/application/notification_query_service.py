class NotificationQueryService:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def get_my_notifications(self, query: object) -> object:
        return {"items": await self._repository.list_for_user(str(getattr(query, "user_id", "")))}
