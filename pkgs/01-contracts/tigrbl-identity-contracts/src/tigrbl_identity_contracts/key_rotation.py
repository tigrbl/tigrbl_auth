from __future__ import annotations

from dataclasses import dataclass

from .evidence import KeyRotationAuditEvidence


@dataclass(frozen=True, slots=True)
class KeyRotationPolicyVersion:
    policy_id: str
    version_id: str
    tenant_id: str
    issuer: str
    profile: str
    key_class: str
    key_use: str
    algorithm: str
    cadence_days: int
    max_key_age_days: int
    overlap_seconds: int
    retirement_seconds: int
    emergency_triggers: tuple[str, ...]
    approval_required: bool
    jwks_publish_required: bool
    created_by: str
    reason: str
    status: str = "draft"
    created_at: str = ""
    approved_by: str | None = None
    approved_at: str | None = None
    published_at: str | None = None
    supersedes: str | None = None


@dataclass(frozen=True, slots=True)
class EffectiveKeyRotationPolicy:
    policy_id: str
    version_id: str
    tenant_id: str
    issuer: str
    profile: str
    key_class: str
    key_use: str
    algorithm: str
    cadence_days: int
    max_key_age_days: int
    overlap_seconds: int
    retirement_seconds: int
    emergency_triggers: tuple[str, ...]
    jwks_publish_required: bool


__all__ = [
    "EffectiveKeyRotationPolicy",
    "KeyRotationAuditEvidence",
    "KeyRotationPolicyVersion",
]
