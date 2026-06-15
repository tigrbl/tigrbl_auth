from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Iterable, Mapping
from uuid import uuid4

from .authority_graph import AuthorityScope
from .delegation_proofs import (
    DelegationAttenuationProof,
    DelegationGrant,
    prove_delegation_attenuation,
)

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


def normalize_delegation_scopes(
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
        return normalize_delegation_scopes(
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


class DelegationGrantLifecycleService:
    def __init__(self) -> None:
        self._grants: dict[str, DelegationGrantLifecycleEntry] = {}
        self._token_links: list[DelegationTokenLink] = []
        self._audit_events: list[DelegationLifecycleAuditEvent] = []

    def create(
        self,
        *,
        delegator: str,
        delegate: str,
        tenant_ids: Iterable[str],
        actions: Iterable[str],
        resources: Iterable[str] | None = None,
        realm: str = "",
        status: str = "active",
        parent_grant_id: str | None = None,
        source_authority_ref: str = "",
        policy_version: str = "",
        provenance_id: str = "",
        constraints: Mapping[str, object] | None = None,
        effective_at: datetime | None = None,
        expires_at: datetime | None = None,
        actor: str | None = None,
    ) -> DelegationGrantLifecycleEntry:
        grant = DelegationGrantLifecycleEntry(
            grant_id=f"dgr:{uuid4()}",
            delegator=delegator,
            delegate=delegate,
            tenant_ids=tuple(tenant_ids),
            actions=tuple(actions),
            resources=tuple(resources or ("*",)),
            realm=realm,
            status=status,
            parent_grant_id=parent_grant_id,
            source_authority_ref=source_authority_ref,
            policy_version=policy_version,
            provenance_id=provenance_id,
            constraints=dict(constraints or {}),
            effective_at=effective_at or _utc_now(),
            expires_at=expires_at,
        )
        self._grants[grant.grant_id] = grant
        self._audit("delegation.grant.created", grant.grant_id, actor=actor)
        if status == "active":
            self._audit("delegation.grant.activated", grant.grant_id, actor=actor)
        return grant

    def inspect(self, grant_id: str) -> DelegationGrantLifecycleEntry:
        try:
            return self._grants[grant_id]
        except KeyError as exc:
            raise KeyError(f"unknown delegation grant {grant_id!r}") from exc

    def list(self, *, tenant_id: str | None = None, delegate: str | None = None) -> tuple[DelegationGrantLifecycleEntry, ...]:
        grants = self._grants.values()
        if tenant_id is not None:
            grants = (grant for grant in grants if tenant_id in grant.tenant_ids)
        if delegate is not None:
            grants = (grant for grant in grants if grant.delegate == delegate)
        return tuple(sorted(grants, key=lambda grant: grant.created_at))

    def activate(self, grant_id: str, *, actor: str | None = None) -> DelegationGrantLifecycleEntry:
        grant = replace(self.inspect(grant_id), status="active", effective_at=_utc_now())
        self._grants[grant_id] = grant
        self._audit("delegation.grant.activated", grant_id, actor=actor)
        return grant

    def revoke(self, grant_id: str, *, actor: str | None = None, reason: str = "revoked") -> tuple[str, ...]:
        revoked_ids = self._revoke_recursive(grant_id, actor=actor, reason=reason)
        if len(revoked_ids) > 1:
            self._audit(
                "delegation.chain.collapsed",
                grant_id,
                actor=actor,
                reason=reason,
                details={"revoked_grant_ids": revoked_ids},
            )
        return revoked_ids

    def expire(self, grant_id: str, *, actor: str | None = None) -> DelegationGrantLifecycleEntry:
        grant = replace(self.inspect(grant_id), status="expired", expires_at=_utc_now())
        self._grants[grant_id] = grant
        self._audit("delegation.grant.expired", grant_id, actor=actor)
        return grant

    def replace(self, grant_id: str, *, actor: str | None = None, **kwargs: object) -> DelegationGrantLifecycleEntry:
        current = self.inspect(grant_id)
        replacement = self.create(
            delegator=str(kwargs.get("delegator") or current.delegator),
            delegate=str(kwargs.get("delegate") or current.delegate),
            tenant_ids=tuple(kwargs.get("tenant_ids") or current.tenant_ids),
            actions=tuple(kwargs.get("actions") or current.actions),
            resources=tuple(kwargs.get("resources") or current.resources),
            realm=str(kwargs.get("realm") or current.realm),
            status=str(kwargs.get("status") or "active"),
            parent_grant_id=grant_id,
            source_authority_ref=str(kwargs.get("source_authority_ref") or current.source_authority_ref),
            policy_version=str(kwargs.get("policy_version") or current.policy_version),
            provenance_id=str(kwargs.get("provenance_id") or current.provenance_id),
            constraints=dict(kwargs.get("constraints") or current.constraints),
            actor=actor,
        )
        revoked = replace(
            current,
            status="replaced",
            revoked_at=_utc_now(),
            revoked_by=actor,
            revoked_reason="replaced",
            replaced_by_grant_id=replacement.grant_id,
        )
        self._grants[grant_id] = revoked
        self._audit("delegation.grant.replaced", grant_id, actor=actor, details={"replacement_grant_id": replacement.grant_id})
        return replacement

    def evaluate(
        self,
        grant_id: str,
        *,
        source_scopes: Iterable[AuthorityScope],
        known_provenance_ids: Iterable[str] | None = None,
        allowed_policy_versions: Iterable[str] | None = None,
        evaluated_at: datetime | None = None,
    ) -> DelegationGrantEvaluation:
        grant = self.inspect(grant_id)
        proof = prove_delegation_attenuation(
            source_scopes=source_scopes,
            grant=grant.to_policy_grant(),
            known_provenance_ids=known_provenance_ids,
            allowed_policy_versions=allowed_policy_versions,
            evaluated_at=(evaluated_at or _utc_now()).isoformat(),
        )
        failures = tuple(proof.failures + (() if grant.active else ("delegation grant is not active",)))
        proof_hash = _stable_hash(
            {
                "grant_id": grant_id,
                "delegated": [scope.key for scope in proof.delegated_scopes],
                "uncovered": [scope.key for scope in proof.uncovered_scopes],
                "failures": failures,
            }
        )
        updated = replace(grant, proof_hash=proof_hash)
        self._grants[grant_id] = updated
        event_type = "delegation.grant.evaluation.allowed" if proof.passed and not failures else "delegation.grant.evaluation.denied"
        self._audit(event_type, grant_id, details={"proof_hash": proof_hash, "failures": failures})
        return DelegationGrantEvaluation(grant_id, proof.passed and not failures, proof, proof_hash, failures)

    def link_token(
        self,
        grant_id: str,
        *,
        token: str,
        subject: str,
        actor_subject: str | None = None,
        token_kind: str = "access",
        authorization_trace_id: str = "",
        delegation_provenance_id: str = "",
        source_token: str | None = None,
        actor_token: str | None = None,
        exchange_mode: str = "delegation",
    ) -> DelegationTokenLink:
        grant = self.inspect(grant_id)
        if not grant.active:
            raise ValueError("cannot link token to inactive delegation grant")
        link = DelegationTokenLink(
            grant_id=grant_id,
            token_hash=_stable_hash(token),
            subject=subject,
            token_kind=token_kind,
            authorization_trace_id=authorization_trace_id,
            delegation_provenance_id=delegation_provenance_id,
            actor_subject=actor_subject,
            exchange_mode=exchange_mode,
            source_token_hash=_stable_hash(source_token) if source_token else None,
            actor_token_hash=_stable_hash(actor_token) if actor_token else None,
        )
        self._token_links.append(link)
        return link

    def token_links(self, grant_id: str | None = None) -> tuple[DelegationTokenLink, ...]:
        links = self._token_links
        if grant_id is not None:
            links = [link for link in links if link.grant_id == grant_id]
        return tuple(links)

    def audit_events(self, grant_id: str | None = None) -> tuple[DelegationLifecycleAuditEvent, ...]:
        events = self._audit_events
        if grant_id is not None:
            events = [event for event in events if event.grant_id == grant_id]
        return tuple(events)

    def management_projection(self, grant_id: str, *, surface: str) -> dict[str, object]:
        assert_delegation_management_surface(surface)
        grant = self.inspect(grant_id)
        return {
            "id": grant.grant_id,
            "status": grant.status,
            "delegator_subject": grant.delegator,
            "delegate_subject": grant.delegate,
            "tenant_ids": list(grant.tenant_ids),
            "actions": list(grant.actions),
            "resources": list(grant.resources),
            "realm": grant.realm,
            "active": grant.active,
            "policy_version": grant.policy_version,
            "provenance_id": grant.provenance_id,
        }

    def _revoke_recursive(self, grant_id: str, *, actor: str | None, reason: str) -> tuple[str, ...]:
        grant = self.inspect(grant_id)
        revoked = replace(grant, status="revoked", revoked_at=_utc_now(), revoked_by=actor, revoked_reason=reason)
        self._grants[grant_id] = revoked
        self._audit("delegation.grant.revoked", grant_id, actor=actor, reason=reason)
        descendants = [
            child.grant_id
            for child in self._grants.values()
            if child.parent_grant_id == grant_id and child.status not in TERMINAL_GRANT_STATUSES
        ]
        revoked_ids = [grant_id]
        for child_id in descendants:
            revoked_ids.extend(self._revoke_recursive(child_id, actor=actor, reason="ancestor-revoked"))
        return tuple(revoked_ids)

    def _audit(
        self,
        event_type: str,
        grant_id: str,
        *,
        actor: str | None = None,
        reason: str | None = None,
        details: Mapping[str, object] | None = None,
    ) -> None:
        self._audit_events.append(
            DelegationLifecycleAuditEvent(
                event_type=event_type,
                grant_id=grant_id,
                actor=actor,
                reason=reason,
                details=dict(details or {}),
            )
        )


def assert_delegation_management_surface(surface: str) -> None:
    if surface not in MANAGEMENT_DELEGATION_SURFACES:
        raise PermissionError(f"{surface!r} cannot manage DelegationGrant lifecycle")


def delegation_grant_uix_workflows(*, surface: str) -> tuple[dict[str, object], ...]:
    assert_delegation_management_surface(surface)
    return tuple({"workflow": workflow, "surface": surface, "api_owned": True} for workflow in DELEGATION_GRANT_UIX_WORKFLOWS)


__all__ = [
    "ACTIVE_GRANT_STATUSES",
    "DELEGATION_GRANT_UIX_WORKFLOWS",
    "MANAGEMENT_DELEGATION_SURFACES",
    "TERMINAL_GRANT_STATUSES",
    "DelegationGrantEvaluation",
    "DelegationGrantLifecycleEntry",
    "DelegationGrantLifecycleService",
    "DelegationLifecycleAuditEvent",
    "DelegationTokenLink",
    "assert_delegation_management_surface",
    "delegation_grant_uix_workflows",
    "normalize_delegation_scopes",
]
