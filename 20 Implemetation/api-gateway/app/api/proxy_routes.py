from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.application.gateway_application_service import GatewayApplicationService

router = APIRouter(prefix="/proxy", tags=["proxy"])
service = GatewayApplicationService()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request) -> JSONResponse:
    """Proxies incoming gateway request to downstream service."""
    body = await request.body()
    result = await service.route_request(request.method, f"/{path}", dict(request.headers), body)
    return JSONResponse(status_code=result["status_code"], content=result["data"])
