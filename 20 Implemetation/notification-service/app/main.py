from fastapi import FastAPI

app = FastAPI(title="notification-service")


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}
