class UserQueryService:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def get_my_profile(self, query: object) -> object:
        return {"user": await self._repository.get(str(getattr(query, "user_id", "")))}

    async def get_user_summary(self, query: object) -> object:
        u = await self._repository.get(str(getattr(query, "user_id", "")))
        if not u:
            return {"user": None}
        return {"user": {"user_id": u["user_id"], "nickname": u.get("nickname"), "status": u.get("status")}}

    async def check_user_exists(self, query: object) -> object:
        return {"exists": await self._repository.get(str(getattr(query, "user_id", ""))) is not None}

    async def get_user_status(self, query: object) -> object:
        u = await self._repository.get(str(getattr(query, "user_id", "")))
        return {"status": None if not u else u.get("status")}
