class NotificationCommandService:
    def __init__(self, dispatch_port: object, repository: object) -> None:
        self._dispatch_port = dispatch_port
        self._repository = repository

    async def dispatch_notification(self, command: object) -> object:
        delivery = await self._dispatch_port.send_notification(command)
        await self.save_notification_log(command)
        return {"success": True, "delivery": delivery}

    async def save_notification_log(self, command: object) -> object:
        payload = {
            "notification_id": str(getattr(command, "notification_id", "")),
            "user_id": str(getattr(command, "user_id", "")),
            "message": str(getattr(command, "message", "")),
            "read": False,
        }
        return await self._repository.save(payload)

    async def mark_notification_as_read(self, command: object) -> object:
        target = str(getattr(command, "notification_id", ""))
        for item in self._repository._logs:
            if item.get("notification_id") == target:
                item["read"] = True
                return {"success": True, "notification": item}
        return {"success": False}
