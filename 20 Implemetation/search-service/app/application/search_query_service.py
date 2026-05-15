from app.infrastructure.in_memory_search_index_repository import InMemorySearchIndexRepository


class SearchQueryService:
    def __init__(self, repository: InMemorySearchIndexRepository) -> None:
        self._repository = repository

    async def search_movies_by_keyword(self, query: object) -> object:
        keyword = str(getattr(query, "keyword", ""))
        return {"items": await self._repository.search(keyword)}

    async def filter_movies_by_genre(self, query: object) -> object:
        genre = str(getattr(query, "genre", "")).lower()
        docs = await self._repository.search("")
        return {"items": [d for d in docs if genre in [g.lower() for g in d.get("genres", [])]]}

    async def filter_movies_by_actor(self, query: object) -> object:
        actor = str(getattr(query, "actor", "")).lower()
        docs = await self._repository.search("")
        return {"items": [d for d in docs if actor in [a.lower() for a in d.get("cast", [])]]}

    async def filter_movies_by_director(self, query: object) -> object:
        director = str(getattr(query, "director", "")).lower()
        docs = await self._repository.search("")
        return {"items": [d for d in docs if director in [a.lower() for a in d.get("directors", [])]]}

    async def filter_movies_by_release_year(self, query: object) -> object:
        year = int(getattr(query, "release_year", 0))
        docs = await self._repository.search("")
        return {"items": [d for d in docs if int(d.get("release_year", 0)) == year]}

    async def filter_movies_by_minimum_rating(self, query: object) -> object:
        minimum = float(getattr(query, "minimum_rating", 0))
        docs = await self._repository.search("")
        return {"items": [d for d in docs if float(d.get("average_rating", 0)) >= minimum]}

    async def search_movies_with_composite_filter(self, query: object) -> object:
        keyword = str(getattr(query, "keyword", ""))
        minimum = float(getattr(query, "minimum_rating", 0))
        docs = await self._repository.search(keyword)
        return {"items": [d for d in docs if float(d.get("average_rating", 0)) >= minimum]}

    async def get_search_index_health(self, query: object) -> object:
        _ = query
        return await self._repository.health()
