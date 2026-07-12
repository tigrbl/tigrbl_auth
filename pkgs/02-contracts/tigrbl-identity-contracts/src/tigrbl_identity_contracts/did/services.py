from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class DidService:
    identifier: str
    service_types: Sequence[str]
    endpoint: str | dict[str, object] | Sequence[object]


__all__ = ["DidService"]
