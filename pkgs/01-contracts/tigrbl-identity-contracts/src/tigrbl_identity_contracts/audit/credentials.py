"""Credential audit event contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from ..credentials.enums import CredentialAuditAction

UTC = timezone.utc


@dataclass(frozen=True, slots=True)
class CredentialAuditEvent:
    id: str
    credential_id: str
    action: CredentialAuditAction
    occurred_at: datetime
    principal_id: str | None = None
    actor: str | None = None
    outcome: str = "ok"
    reason: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "action", CredentialAuditAction(self.action))
        if self.occurred_at.tzinfo is None:
            object.__setattr__(self, "occurred_at", self.occurred_at.replace(tzinfo=UTC))
        else:
            object.__setattr__(self, "occurred_at", self.occurred_at.astimezone(UTC))


__all__ = ["CredentialAuditEvent"]
