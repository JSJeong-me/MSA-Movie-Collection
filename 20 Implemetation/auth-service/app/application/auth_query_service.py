class AuthQueryService:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def verify_access_token(self, query: object) -> object:
        token = str(getattr(query, "access_token", ""))
        if not token.startswith("access-"):
            return {"valid": False}
        user_id = token.split("-")[1]
        cred = await self._repository.get_credential(user_id)
        return {"valid": bool(cred and cred.get("active", False)), "user_id": user_id, "role": cred.get("role", "user") if cred else None}

    async def get_user_role(self, query: object) -> object:
        cred = await self._repository.get_credential(str(getattr(query, "user_id", "")))
        return {"role": None if not cred else cred.get("role")}

    async def validate_password(self, query: object) -> object:
        cred = await self._repository.get_credential(str(getattr(query, "user_id", "")))
        return {"match": bool(cred and cred.get("password") == str(getattr(query, "password", "")))}

    async def is_token_revoked(self, query: object) -> object:
        token = await self._repository.get_token(str(getattr(query, "refresh_token", "")))
        return {"revoked": bool(token and token.get("revoked"))}
