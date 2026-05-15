from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class EventEnvelope(Generic[T]):
    event_id: str
    event_type: str
    occurred_at: datetime
    source: str
    payload: T
