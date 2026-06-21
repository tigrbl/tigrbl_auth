from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, Mapping

from ..authority import AuthorityScope
from .proofs import DelegationAttenuationProof, DelegationGrant

ACTIVE_GRANT_STATUSES = {"active"}
TERMINAL_GRANT_STATUSES = {"revoked", "expired", "replaced"}
MANAGEMENT_DELEGATION_SURFACES = {
    "platform-admin-api",
    "tenant-admin-api",
    "developer-api",
    "service-admin-api",
}
DELEGATION_GRANT_UIX_WORKFLOWS = (
    "list",
    "inspect",
    "create",
    "replace",
    "revoke",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def _normalize_values(values: Iterable[str] | None, *, default: tuple[str, ...] = ()) -> tuple[str, ...]:
    normalized = {str(value).strip() for value in values or default if str(value).strip()}
    return tuple(sorted(normalized))


def _normalize_delegation_scopes(
    *,
    tenant_ids: Iterable[str],
    actions: Iterable[str],
    resources: Iterable[str] | None = None,
    realm: str = "",
) -> tuple[AuthorityScope, ...]:
    tenants = _normalize_values(tenant_ids)
    normalized_actions = _normalize_values(actions)
    normalized_resources = _normalize_values(resources, default=("*",))
    if not tenants:
        raise ValueError("at least one tenant_id is required")
    if not normalized_actions:
        raise ValueError("at least one action is required")
    return tuple(
        AuthorityScope(tenant_id=tenant, realm=realm, action=action, resource=resource)
        for tenant in tenants
        for action in normalized_actions
        for resource in normalized_resources
    )


@dataclass(frozen=True, slots=True)
class DelegationLifecycleAuditEvent:
    event_type: str
    grant_id: str
    actor: str | None = None
    reason: str | None = None
    occurred_at: datetime = field(default_factory=_utc_now)
    details: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DelegationTokenLink:
    grant_id: str
    token_hash: str
    subject: str
    token_kind: str = "access"
    authorization_trace_id: str = ""
    delegation_provenance_id: str = ""
    actor_subject: str | None = None
    exchange_mode: str = "delegation"
    source_token_hash: str | None = None
    actor_token_hash: str | None = None

    def as_claims(self) -> dict[str, object]:
        return {
            "delegation_grant_id": self.grant_id,
            "delegation_token_hash": self.token_hash,
            "delegation_provenance_id": self.delegation_provenance_id,
            "authorization_trace_id": self.authorization_trace_id,
            "actor_subject": self.actor_subject,
            "subject": self.subject,
            "exchange_mode": self.exchange_mode,
            "source_token_hash": self.source_token_hash,
            "actor_token_hash": self.actor_token_hash,
        }


@dataclass(frozen=True, slots=True)
class DelegationGrantLifecycleEntry:
    grant_id: str
    delegator: str
    delegate: str
    tenant_ids: tuple[str, ...]
    actions: tuple[str, ...]
    resources: tuple[str, ...] = ("*",)
    realm: str = ""
    status: str = "draft"
    parent_grant_id: str | None = None
    source_authority_ref: str = ""
    policy_version: str = ""
    provenance_id: str = ""
    constraints: Mapping[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)
    effective_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    revoked_by: str | None = None
    revoked_reason: str | None = None
    replaced_by_grant_id: str | None = None
    proof_hash: str = ""

    def __post_init__(self) -> None:
        if not self.delegator or not self.delegate:
            raise ValueError("delegator and delegate are required")
        object.__setattr__(self, "tenant_ids", _normalize_values(self.tenant_ids))
        object.__setattr__(self, "actions", _normalize_values(self.actions))
        object.__setattr__(self, "resources", _normalize_values(self.resources, default=("*",)))
        if not self.tenant_ids:
            raise ValueError("tenant_ids are required")
        if not self.actions:
            raise ValueError("actions are required")

    @property
    def active(self) -> bool:
        if self.status not in ACTIVE_GRANT_STATUSES:
            return False
        if self.expires_at is not None and self.expires_at <= _utc_now():
            return False
        return self.revoked_at is None

    def to_policy_grant(self) -> DelegationGrant:
        return DelegationGrant(
            delegator=self.delegator,
            delegate=self.delegate,
            tenant_ids=self.tenant_ids,
            actions=self.actions,
            resources=self.resources,
            realm=self.realm,
            policy_version=self.policy_version,
            provenance_id=self.provenance_id,
            revoked=self.revoked_at is not None or self.status in TERMINAL_GRANT_STATUSES,
            expires_at=self.expires_at.isoformat() if self.expires_at else None,
        )

    def scopes(self) -> tuple[AuthorityScope, ...]:
        return _normalize_delegation_scopes(
            tenant_ids=self.tenant_ids,
            actions=self.actions,
            resources=self.resources,
            realm=self.realm,
        )


@dataclass(frozen=True, slots=True)
class DelegationGrantEvaluation:
    grant_id: str
    allowed: bool
    proof: DelegationAttenuationProof
    proof_hash: str
    failures: tuple[str, ...]


__all__ = [
    "ACTIVE_GRANT_STATUSES",
    "DELEGATION_GRANT_UIX_WORKFLOWS",
    "MANAGEMENT_DELEGATION_SURFACES",
    "TERMINAL_GRANT_STATUSES",
    "DelegationGrantEvaluation",
    "DelegationGrantLifecycleEntry",
    "DelegationLifecycleAuditEvent",
    "DelegationTokenLink",
    "_stable_hash",
    "_utc_now",
]
