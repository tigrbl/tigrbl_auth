"""Administrative audit event contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..admin_resources import AdminResourceKind, _utc_now


@dataclass(frozen=True, slots=True)
class AdminAuditEvent:
    event_id: str
    actor: str
    action: str
    resource_kind: AdminResourceKind
    resource_id: str
    tenant_id: str
    outcome: str
    recorded_at: str = field(default_factory=_utc_now)


__all__ = ["AdminAuditEvent"]
