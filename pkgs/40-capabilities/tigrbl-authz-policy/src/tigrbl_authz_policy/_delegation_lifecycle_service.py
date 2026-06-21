from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now
from tigrbl_identity_core.json_canonicalization import canonical_hash
from tigrbl_identity_contracts.delegation import (
    DELEGATION_GRANT_UIX_WORKFLOWS,
    MANAGEMENT_DELEGATION_SURFACES,
    TERMINAL_GRANT_STATUSES,
    DelegationGrantEvaluation,
    DelegationGrantLifecycleEntry,
    DelegationLifecycleAuditEvent,
    DelegationTokenLink,
)

from .authority_graph import AuthorityScope
from .delegation_proofs import prove_delegation_attenuation


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
            effective_at=effective_at or utc_now(),
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
        grant = replace(self.inspect(grant_id), status="active", effective_at=utc_now())
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
        grant = replace(self.inspect(grant_id), status="expired", expires_at=utc_now())
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
            revoked_at=utc_now(),
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
            evaluated_at=(evaluated_at or utc_now()).isoformat(),
        )
        failures = tuple(proof.failures + (() if grant.active else ("delegation grant is not active",)))
        proof_hash = canonical_hash(
            {
                "grant_id": grant_id,
                "delegated": [scope.key for scope in proof.delegated_scopes],
                "uncovered": [scope.key for scope in proof.uncovered_scopes],
                "failures": failures,
            }
        )
        self._grants[grant_id] = replace(grant, proof_hash=proof_hash)
        event_type = "delegation.grant.evaluation.allowed" if proof.passed and not failures else "delegation.grant.evaluation.denied"
        self._audit(event_type, grant_id, details={"proof_hash": proof_hash, "failures": failures})
        return DelegationGrantEvaluation(grant_id, proof.passed and not failures, proof, proof_hash, failures)

    def link_token(self, grant_id: str, *, token: str, subject: str, **kwargs: object) -> DelegationTokenLink:
        grant = self.inspect(grant_id)
        if not grant.active:
            raise ValueError("cannot link token to inactive delegation grant")
        link = DelegationTokenLink(
            grant_id=grant_id,
            token_hash=canonical_hash(token),
            subject=subject,
            token_kind=str(kwargs.get("token_kind") or "access"),
            authorization_trace_id=str(kwargs.get("authorization_trace_id") or ""),
            delegation_provenance_id=str(kwargs.get("delegation_provenance_id") or ""),
            actor_subject=kwargs.get("actor_subject") if isinstance(kwargs.get("actor_subject"), str) else None,
            exchange_mode=str(kwargs.get("exchange_mode") or "delegation"),
            source_token_hash=canonical_hash(kwargs["source_token"]) if isinstance(kwargs.get("source_token"), str) else None,
            actor_token_hash=canonical_hash(kwargs["actor_token"]) if isinstance(kwargs.get("actor_token"), str) else None,
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
        self._grants[grant_id] = replace(grant, status="revoked", revoked_at=utc_now(), revoked_by=actor, revoked_reason=reason)
        self._audit("delegation.grant.revoked", grant_id, actor=actor, reason=reason)
        revoked_ids = [grant_id]
        descendants = [
            child.grant_id
            for child in self._grants.values()
            if child.parent_grant_id == grant_id and child.status not in TERMINAL_GRANT_STATUSES
        ]
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
    "DelegationGrantLifecycleService",
    "assert_delegation_management_surface",
    "delegation_grant_uix_workflows",
]
