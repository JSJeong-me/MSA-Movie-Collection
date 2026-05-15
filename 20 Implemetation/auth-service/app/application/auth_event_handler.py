class AuthEventHandler:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def create_credential_for_user(self, event: object) -> object:
        payload = getattr(event, "payload", {})
        await self._repository.set_credential(payload.get("user_id", ""), payload.get("password", "changeme"))
        return {"success": True}

    async def deactivate_credential(self, event: object) -> object:
        payload = getattr(event, "payload", {})
        cred = await self._repository.get_credential(payload.get("user_id", ""))
        if not cred:
            return {"success": False}
        cred["active"] = False
        return {"success": True}
