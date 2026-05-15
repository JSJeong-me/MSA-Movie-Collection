from types import SimpleNamespace

from tests.helpers import load_service_module


async def _collection_happy_path():
    services = load_service_module("collection-service", "app.services")
    create_cmd = SimpleNamespace(
        collection_id="c1",
        owner_id="u1",
        title="Favorites",
        description="my picks",
        visibility="private",
    )
    created = await services.collection_command_service.create_collection(create_cmd)

    add_cmd = SimpleNamespace(collection_id="c1", movie_id="m1", owner_id="u1")
    added = await services.collection_command_service.add_movie_to_collection(add_cmd)

    items = await services.collection_query_service.get_collection_items(SimpleNamespace(collection_id="c1"))
    return created, added, items


async def _collection_duplicate_case():
    services = load_service_module("collection-service", "app.services")
    await services.collection_command_service.create_collection(
        SimpleNamespace(collection_id="c2", owner_id="u1", title="Watched", description="", visibility="private")
    )
    cmd = SimpleNamespace(collection_id="c2", movie_id="m2", owner_id="u1")
    first = await services.collection_command_service.add_movie_to_collection(cmd)
    second = await services.collection_command_service.add_movie_to_collection(cmd)
    return first, second


def test_scenario_add_movie_to_collection_success(anyio_backend):
    import anyio

    created, added, items = anyio.run(_collection_happy_path)
    assert created["success"] is True
    assert added["success"] is True
    assert items["items"] == ["m1"]


def test_scenario_duplicate_movie_addition_is_rejected(anyio_backend):
    import anyio

    first, second = anyio.run(_collection_duplicate_case)
    assert first["success"] is True
    assert second["success"] is False
    assert second["reason"] == "already added"
