class InMemoryNotificationRepository:
    def __init__(self) -> None:
        self._logs: list[dict] = []

    async def save(self, log: dict) -> dict:
        self._logs.append(log)
        return log

    async def list_for_user(self, user_id: str) -> list[dict]:
        return [x for x in self._logs if x.get("user_id") == user_id]
