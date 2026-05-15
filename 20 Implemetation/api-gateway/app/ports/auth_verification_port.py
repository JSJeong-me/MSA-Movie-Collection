from typing import Protocol


class AuthVerificationPort(Protocol):
    async def verify_access_token_for_gateway(self, query: object) -> object:
        ...

    async def resolve_user_role_for_gateway(self, query: object) -> object:
        ...
