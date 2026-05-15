from dataclasses import dataclass


@dataclass(frozen=True)
class AuthContext:
    """Authenticated identity propagated from gateway."""

    user_id: str
    role: str
