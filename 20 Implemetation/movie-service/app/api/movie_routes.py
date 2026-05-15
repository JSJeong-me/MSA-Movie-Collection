from types import SimpleNamespace

from fastapi import APIRouter, Body, Query

from app.services import movie_command_service, movie_query_service


router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def get_movie_list_route(page: int = Query(default=1), size: int = Query(default=20)) -> object:
    query = SimpleNamespace(page=page, size=size)
    return await movie_query_service.get_movie_list(query)


@router.get("/{movie_id}")
async def get_movie_detail_route(movie_id: str) -> object:
    query = SimpleNamespace(movie_id=movie_id)
    return await movie_query_service.get_movie_detail(query)


@router.post("")
async def create_movie_route(command: dict = Body(...)) -> object:
    return await movie_command_service.create_movie(SimpleNamespace(**command))
