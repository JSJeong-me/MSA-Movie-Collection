from fastapi import FastAPI

from app.api.movie_routes import router as movie_router


def create_app() -> FastAPI:
    app = FastAPI(title="movie-service")
    app.include_router(movie_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
