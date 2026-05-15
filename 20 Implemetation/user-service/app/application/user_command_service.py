class UserCommandService:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def register_user(self, command: object) -> object:
        user = {
            "user_id": str(getattr(command, "user_id", "")),
            "nickname": str(getattr(command, "nickname", "")),
            "status": "active",
            "profile_image": None,
        }
        await self._repository.create(user)
        return {"success": True, "user": user}

    async def update_my_profile(self, command: object) -> object:
        updated = await self._repository.update(str(getattr(command, "user_id", "")), dict(getattr(command, "patch", {})))
        return {"success": updated is not None, "user": updated}

    async def deactivate_my_account(self, command: object) -> object:
        updated = await self._repository.update(str(getattr(command, "user_id", "")), {"status": "deactivated"})
        return {"success": updated is not None}

    async def update_profile_image(self, command: object) -> object:
        updated = await self._repository.update(str(getattr(command, "user_id", "")), {"profile_image": str(getattr(command, "profile_image", ""))})
        return {"success": updated is not None, "user": updated}
