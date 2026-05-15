class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}

    async def create(self, user: dict) -> dict:
        self._users[user["user_id"]] = user
        return user

    async def get(self, user_id: str) -> dict | None:
        return self._users.get(user_id)

    async def update(self, user_id: str, patch: dict) -> dict | None:
        u = self._users.get(user_id)
        if not u:
            return None
        u.update(patch)
        return u
