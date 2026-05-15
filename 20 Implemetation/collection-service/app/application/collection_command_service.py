class CollectionCommandService:
    def __init__(self, repository: object, movie_validation_port: object) -> None:
        self._repository = repository
        self._movie_validation_port = movie_validation_port

    async def create_collection(self, command: object) -> object:
        collection = {
            "collection_id": str(getattr(command, "collection_id", "")),
            "owner_id": str(getattr(command, "owner_id", "")),
            "title": str(getattr(command, "title", "")),
            "description": str(getattr(command, "description", "")),
            "visibility": str(getattr(command, "visibility", "private")),
            "items": [],
        }
        await self._repository.create(collection)
        return {"success": True, "collection": collection}

    async def update_collection(self, command: object) -> object:
        updated = await self._repository.update(str(getattr(command, "collection_id", "")), dict(getattr(command, "patch", {})))
        return {"success": updated is not None, "collection": updated}

    async def delete_collection(self, command: object) -> object:
        deleted = await self._repository.delete(str(getattr(command, "collection_id", "")))
        return {"success": deleted}

    async def add_movie_to_collection(self, command: object) -> object:
        collection_id = str(getattr(command, "collection_id", ""))
        movie_id = str(getattr(command, "movie_id", ""))
        exists = await self._movie_validation_port.verify_movie_exists_for_collection(command)
        if not exists.get("exists", False):
            return {"success": False, "reason": "movie does not exist"}
        collection = await self._repository.get(collection_id)
        if not collection:
            return {"success": False, "reason": "collection not found"}
        if movie_id in collection["items"]:
            return {"success": False, "reason": "already added"}
        collection["items"].append(movie_id)
        return {"success": True, "collection": collection}

    async def remove_movie_from_collection(self, command: object) -> object:
        collection = await self._repository.get(str(getattr(command, "collection_id", "")))
        movie_id = str(getattr(command, "movie_id", ""))
        if not collection or movie_id not in collection["items"]:
            return {"success": False}
        collection["items"].remove(movie_id)
        return {"success": True, "collection": collection}
