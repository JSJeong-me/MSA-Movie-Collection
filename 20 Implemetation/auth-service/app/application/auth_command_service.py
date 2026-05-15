import uuid


class AuthCommandService:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def login_user(self, command: object) -> object:
        user_id = str(getattr(command, "user_id", ""))
        password = str(getattr(command, "password", ""))
        cred = await self._repository.get_credential(user_id)
        if not cred or cred.get("password") != password or not cred.get("active", False):
            return {"success": False}
        access_token = f"access-{user_id}-{uuid.uuid4()}"
        refresh_token = f"refresh-{user_id}-{uuid.uuid4()}"
        await self._repository.save_token(refresh_token, {"user_id": user_id})
        return {"success": True, "access_token": access_token, "refresh_token": refresh_token, "role": cred.get("role", "user")}

    async def logout_user(self, command: object) -> object:
        token = await self._repository.get_token(str(getattr(command, "refresh_token", "")))
        if not token:
            return {"success": False}
        token["revoked"] = True
        return {"success": True}

    async def refresh_access_token(self, command: object) -> object:
        refresh_token = str(getattr(command, "refresh_token", ""))
        token = await self._repository.get_token(refresh_token)
        if not token or token.get("revoked"):
            return {"success": False}
        return {"success": True, "access_token": f"access-{token['user_id']}-{uuid.uuid4()}"}

    async def update_user_role(self, command: object) -> object:
        user_id = str(getattr(command, "user_id", ""))
        role = str(getattr(command, "role", "user"))
        cred = await self._repository.get_credential(user_id)
        if not cred:
            return {"success": False}
        cred["role"] = role
        return {"success": True, "user_id": user_id, "role": role}
