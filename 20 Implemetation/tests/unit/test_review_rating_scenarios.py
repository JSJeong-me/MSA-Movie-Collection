from types import SimpleNamespace

from tests.helpers import load_service_module


async def _review_and_rating_flow():
    services = load_service_module("review-service", "app.services")

    created_review = await services.review_command_service.create_review(
        SimpleNamespace(review_id="r1", movie_id="m9", user_id="u9", content="great")
    )
    reviews = await services.review_query_service.get_reviews_by_movie(SimpleNamespace(movie_id="m9"))

    rating = await services.rating_command_service.create_or_update_rating(
        SimpleNamespace(movie_id="m9", user_id="u9", score=5)
    )
    summary = await services.review_query_service.get_rating_summary_by_movie(SimpleNamespace(movie_id="m9"))
    return created_review, reviews, rating, summary


def test_scenario_create_review_and_query_by_movie(anyio_backend):
    import anyio

    created_review, reviews, _, _ = anyio.run(_review_and_rating_flow)
    assert created_review["success"] is True
    assert len(reviews["items"]) == 1
    assert reviews["items"][0]["content"] == "great"


def test_scenario_rating_update_reflected_in_summary(anyio_backend):
    import anyio

    _, _, rating, summary = anyio.run(_review_and_rating_flow)
    assert rating["success"] is True
    assert summary["count"] >= 1
    assert summary["average"] >= 1.0
