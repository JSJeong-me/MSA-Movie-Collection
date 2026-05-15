from typing import Protocol


class NotificationDispatchPort(Protocol):
    async def send_notification(self, command: object) -> object:
        ...
