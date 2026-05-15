from fastapi import FastAPI

from app.api.proxy_routes import router as proxy_router

app = FastAPI(title="api-gateway")
app.include_router(proxy_router)


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}
