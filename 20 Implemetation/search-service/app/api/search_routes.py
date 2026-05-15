from types import SimpleNamespace

from fastapi import APIRouter, Query

from app.services import search_query_service


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/movies")
async def search_movies_route(q: str = Query(default=""), minimum_rating: float = Query(default=0.0)) -> object:
    query = SimpleNamespace(keyword=q, minimum_rating=minimum_rating)
    return await search_query_service.search_movies_with_composite_filter(query)
