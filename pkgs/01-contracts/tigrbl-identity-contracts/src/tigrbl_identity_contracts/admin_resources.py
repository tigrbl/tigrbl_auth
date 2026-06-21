from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

from tigrbl_identity_core.clock import utc_now_iso


class AdminResourceKind(str, Enum):
    PRINCIPAL = "principal"
    CREDENTIAL = "credential"
    APP = "app"
    SERVICE_IDENTITY = "service_identity"
    RESOURCE_SERVER = "resource_server"
    POLICY = "policy"


class AdminResourceStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"


def _clean_tuple(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


@dataclass(frozen=True, slots=True)
class AdminResource:
    id: str
    kind: AdminResourceKind
    tenant_id: str
    name: str
    status: AdminResourceStatus = AdminResourceStatus.ACTIVE
    attributes: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.id or not self.tenant_id or not self.name:
            raise ValueError("admin resource requires id, tenant_id, and name")
        object.__setattr__(self, "kind", AdminResourceKind(self.kind))
        object.__setattr__(self, "status", AdminResourceStatus(self.status))
        object.__setattr__(self, "attributes", dict(self.attributes))


__all__ = [
    "AdminResource",
    "AdminResourceKind",
    "AdminResourceStatus",
]
