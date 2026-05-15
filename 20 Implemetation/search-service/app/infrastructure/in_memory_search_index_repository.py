class InMemorySearchIndexRepository:
    def __init__(self) -> None:
        self._docs: dict[str, dict] = {}

    async def upsert(self, movie_id: str, doc: dict) -> None:
        self._docs[movie_id] = doc

    async def delete(self, movie_id: str) -> None:
        self._docs.pop(movie_id, None)

    async def get(self, movie_id: str) -> dict | None:
        return self._docs.get(movie_id)

    async def search(self, keyword: str) -> list[dict]:
        if not keyword:
            return list(self._docs.values())
        low = keyword.lower()
        return [doc for doc in self._docs.values() if low in str(doc.get("title", "")).lower()]

    async def health(self) -> dict:
        return {"status": "ok", "documents": len(self._docs)}
