from types import SimpleNamespace

from fastapi import APIRouter, Body, Query

from app.services import review_command_service, review_query_service


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("")
async def create_review_route(command: dict = Body(...)) -> object:
    return await review_command_service.create_review(SimpleNamespace(**command))


@router.get("")
async def get_reviews_by_movie_route(movie_id: str = Query(...)) -> object:
    return await review_query_service.get_reviews_by_movie(SimpleNamespace(movie_id=movie_id))
