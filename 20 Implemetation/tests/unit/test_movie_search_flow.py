from types import SimpleNamespace

from tests.helpers import load_service_module


async def _create_movie_and_search():
    search_services = load_service_module("search-service", "app.services")
    movie_services = load_service_module("movie-service", "app.services")

    create_command = SimpleNamespace(
        movie_id="mv-1",
        title="Interstellar",
        description="space travel",
        release_year=2014,
        genres=["Sci-Fi"],
        cast=["Matthew McConaughey"],
        directors=["Christopher Nolan"],
    )
    created = await movie_services.movie_command_service.create_movie(create_command)

    query = SimpleNamespace(keyword="Interstellar", minimum_rating=0.0)
    searched = await search_services.search_query_service.search_movies_with_composite_filter(query)
    return created, searched


def test_scenario_movie_created_event_updates_search_index(anyio_backend):
    import anyio

    created, searched = anyio.run(_create_movie_and_search)
    assert created["success"] is True
    assert len(searched["items"]) == 1
    assert searched["items"][0]["title"] == "Interstellar"
