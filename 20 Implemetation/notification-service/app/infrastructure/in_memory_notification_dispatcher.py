class InMemoryNotificationDispatcher:
    async def send_notification(self, command: object) -> object:
        return {"delivered": True, "channel": getattr(command, "channel", "in-app")}
