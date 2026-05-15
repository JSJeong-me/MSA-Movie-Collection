from shared.contexts.auth_context import AuthContext
from shared.contexts.request_context import RequestContext


class GatewayApplicationService:
    async def route_request(self, client_request: object) -> object:
        path = str(getattr(client_request, "path", "/"))
        if path.startswith("/movies"):
            return {"target_service": "movie-service", "path": path}
        if path.startswith("/collections"):
            return {"target_service": "collection-service", "path": path}
        if path.startswith("/reviews"):
            return {"target_service": "review-service", "path": path}
        if path.startswith("/search"):
            return {"target_service": "search-service", "path": path}
        return {"target_service": "unknown", "path": path}

    async def authenticate_request(self, authorization_header: str) -> AuthContext:
        token = authorization_header.replace("Bearer", "").strip()
        user_id = token if token else "anonymous"
        role = "admin" if user_id.startswith("admin") else "user"
        return AuthContext(user_id=user_id, role=role)

    async def authorize_request(self, auth_context: AuthContext, access_policy: object) -> object:
        required_role = str(getattr(access_policy, "required_role", "user"))
        allow = auth_context.role == required_role or auth_context.role == "admin"
        return {"allow": allow, "required_role": required_role, "actual_role": auth_context.role}

    async def enrich_request_context(
        self,
        routed_request: object,
        auth_context: AuthContext | None,
        request_context: RequestContext,
    ) -> object:
        return {
            "routed_request": routed_request,
            "request_id": request_context.request_id,
            "correlation_id": request_context.correlation_id,
            "user_id": auth_context.user_id if auth_context else None,
            "role": auth_context.role if auth_context else None,
        }

    async def apply_rate_limit(self, client_identity: object, route_policy: object) -> object:
        _ = (client_identity, route_policy)
        return {"allow": True, "reason": "within_limit"}

    async def normalize_error_response(self, downstream_error: object) -> object:
        return {"code": "DOWNSTREAM_ERROR", "message": str(downstream_error)}

    async def write_access_log(self, request_context: RequestContext, response_context: object) -> None:
        _ = (request_context, response_context)
        return None
