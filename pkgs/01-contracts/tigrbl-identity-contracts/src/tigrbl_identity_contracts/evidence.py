from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KeyRotationAuditEvidence:
    audit_id: str
    tenant_id: str
    issuer: str
    profile: str
    policy_id: str
    policy_version_id: str
    actor: str
    old_kid: str
    new_kid: str
    authorization_decision_ref: str
    jwks_published: bool
    retired: bool
    reason: str
    recorded_at: str


__all__ = ["KeyRotationAuditEvidence"]
