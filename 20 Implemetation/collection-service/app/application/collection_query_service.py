class CollectionQueryService:
    def __init__(self, repository: object) -> None:
        self._repository = repository

    async def get_my_collections(self, query: object) -> object:
        owner_id = str(getattr(query, "owner_id", ""))
        return {"items": await self._repository.list_by_owner(owner_id)}

    async def get_collection_detail(self, query: object) -> object:
        return {"collection": await self._repository.get(str(getattr(query, "collection_id", "")))}

    async def get_collection_items(self, query: object) -> object:
        collection = await self._repository.get(str(getattr(query, "collection_id", "")))
        return {"items": [] if not collection else collection.get("items", [])}

    async def check_collection_ownership(self, query: object) -> object:
        c = await self._repository.get(str(getattr(query, "collection_id", "")))
        return {"owned": bool(c and c.get("owner_id") == str(getattr(query, "owner_id", "")))}

    async def check_movie_already_added(self, query: object) -> object:
        c = await self._repository.get(str(getattr(query, "collection_id", "")))
        movie_id = str(getattr(query, "movie_id", ""))
        return {"already_added": bool(c and movie_id in c.get("items", []))}
