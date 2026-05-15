from fastapi import FastAPI

from app.api.collection_routes import router as collection_router


def create_app() -> FastAPI:
    app = FastAPI(title="collection-service")
    app.include_router(collection_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
