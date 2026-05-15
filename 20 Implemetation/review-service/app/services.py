from app.application.rating_command_service import RatingCommandService
from app.application.review_command_service import ReviewCommandService
from app.application.review_query_service import ReviewQueryService
from app.events.review_events import ReviewEventPublisher
from app.infrastructure.in_memory_rating_repository import InMemoryRatingRepository
from app.infrastructure.in_memory_review_repository import InMemoryReviewRepository
from app.infrastructure.in_memory_event_publisher import InMemoryEventPublisher


class _MovieValidationAdapter:
    async def verify_movie_exists_for_review(self, query: object) -> object:
        return {"exists": bool(getattr(query, "movie_id", ""))}


review_repository = InMemoryReviewRepository()
rating_repository = InMemoryRatingRepository()
review_event_publisher = ReviewEventPublisher(InMemoryEventPublisher())
movie_validation_port = _MovieValidationAdapter()
review_command_service = ReviewCommandService(review_repository, movie_validation_port, review_event_publisher)
rating_command_service = RatingCommandService(rating_repository, movie_validation_port, review_event_publisher)
review_query_service = ReviewQueryService(review_repository, rating_repository)
