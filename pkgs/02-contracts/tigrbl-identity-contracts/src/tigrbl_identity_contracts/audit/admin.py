"""Administrative audit event contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field

from tigrbl_identity_core.clock import utc_now_iso

from ..admin_resources import AdminResourceKind


@dataclass(frozen=True, slots=True)
class AdminAuditEvent:
    event_id: str
    actor: str
    action: str
    resource_kind: AdminResourceKind
    resource_id: str
    tenant_id: str
    outcome: str
    recorded_at: str = field(default_factory=utc_now_iso)


__all__ = ["AdminAuditEvent"]
