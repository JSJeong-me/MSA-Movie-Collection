from fastapi import FastAPI

from app.api.search_routes import router as search_router


def create_app() -> FastAPI:
    app = FastAPI(title="search-service")
    app.include_router(search_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
