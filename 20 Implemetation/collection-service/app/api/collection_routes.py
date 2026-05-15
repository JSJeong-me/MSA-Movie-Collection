from types import SimpleNamespace

from fastapi import APIRouter, Body

from app.services import collection_command_service


router = APIRouter(prefix="/collections", tags=["Collections"])


@router.post("")
async def create_collection_route(command: dict = Body(...)) -> object:
    return await collection_command_service.create_collection(SimpleNamespace(**command))


@router.post("/{collection_id}/items")
async def add_movie_to_collection_route(collection_id: str, command: dict = Body(...)) -> object:
    payload = dict(command)
    payload["collection_id"] = collection_id
    return await collection_command_service.add_movie_to_collection(SimpleNamespace(**payload))
