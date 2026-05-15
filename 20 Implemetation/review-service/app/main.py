from fastapi import FastAPI

from app.api.review_routes import router as review_router


def create_app() -> FastAPI:
    app = FastAPI(title="review-service")
    app.include_router(review_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
