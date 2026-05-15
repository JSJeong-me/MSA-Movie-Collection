class InMemoryAuthRepository:
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}
        self._tokens: dict[str, dict] = {}

    async def set_credential(self, user_id: str, password: str, role: str = "user") -> None:
        self._users[user_id] = {"password": password, "role": role, "active": True}

    async def get_credential(self, user_id: str) -> dict | None:
        return self._users.get(user_id)

    async def save_token(self, refresh_token: str, payload: dict) -> None:
        self._tokens[refresh_token] = {**payload, "revoked": False}

    async def get_token(self, refresh_token: str) -> dict | None:
        return self._tokens.get(refresh_token)
