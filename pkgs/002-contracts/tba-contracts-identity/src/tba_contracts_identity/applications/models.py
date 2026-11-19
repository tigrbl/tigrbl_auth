from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


def _normalize(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


@dataclass(frozen=True, slots=True)
class App:
    id: str
    tenant_id: str
    name: str
    client_ids: tuple[str, ...] = ()
    owner_principal_id: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("app id is required")
        if not self.tenant_id:
            raise ValueError("app tenant_id is required")
        if not self.name:
            raise ValueError("app name is required")
        object.__setattr__(self, "client_ids", _normalize(self.client_ids))
        object.__setattr__(self, "attributes", dict(self.attributes))


__all__ = ["App"]
