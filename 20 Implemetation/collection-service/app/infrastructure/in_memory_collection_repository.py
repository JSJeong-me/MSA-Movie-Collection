class InMemoryCollectionRepository:
    def __init__(self) -> None:
        self._collections: dict[str, dict] = {}

    async def create(self, collection: dict) -> dict:
        self._collections[collection["collection_id"]] = collection
        return collection

    async def get(self, collection_id: str) -> dict | None:
        return self._collections.get(collection_id)

    async def update(self, collection_id: str, patch: dict) -> dict | None:
        c = self._collections.get(collection_id)
        if c is None:
            return None
        c.update(patch)
        return c

    async def delete(self, collection_id: str) -> bool:
        return self._collections.pop(collection_id, None) is not None

    async def list_by_owner(self, owner_id: str) -> list[dict]:
        return [c for c in self._collections.values() if c.get("owner_id") == owner_id]
