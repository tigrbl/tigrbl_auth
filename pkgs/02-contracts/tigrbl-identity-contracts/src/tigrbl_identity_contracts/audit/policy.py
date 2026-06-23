"""Policy audit event contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolicyAuditEvent:
    event_id: str
    subject: str
    tenant_id: str | None
    permission: str
    allowed: bool
    reason: str
    matched: tuple[str, ...]
    actor_type: str
    recorded_at: str
    client_id: str | None = None


__all__ = ["PolicyAuditEvent"]
