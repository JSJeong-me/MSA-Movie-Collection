from fastapi import FastAPI

app = FastAPI(title="user-service")


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}
