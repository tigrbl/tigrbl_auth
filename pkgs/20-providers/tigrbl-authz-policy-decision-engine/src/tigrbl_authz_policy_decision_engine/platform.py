"""Deterministic platform PDP with default deny and proof lineage."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Iterable
from uuid import uuid4

from tigrbl_authorization_contracts import (
    ActionDefinition, AuthorizationDecision, AuthorizationEffect, AuthorizationRequest,
    RoleDefinition, RoleGrant,
)


class PlatformPolicyDecisionEngine:
    def __init__(self, *, actions: Iterable[ActionDefinition], roles: Iterable[RoleDefinition] = (), grants: Iterable[RoleGrant] = (), policy_version: str = "unpublished", clock: Callable[[], datetime] | None = None) -> None:
        self._actions = {item.key: item for item in actions}
        self._roles = {item.role_id: item for item in roles}
        self._grants = tuple(grants)
        self._policy_version = policy_version
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._decisions: list[AuthorizationDecision] = []

    @property
    def decisions(self) -> tuple[AuthorizationDecision, ...]:
        return tuple(self._decisions)

    def _record(self, decision: AuthorizationDecision) -> AuthorizationDecision:
        self._decisions.append(decision)
        return decision

    def _deny(self, reason: str, *, obligations: tuple[str, ...] = (), grants: tuple[str, ...] = (), roles: tuple[str, ...] = (), missing_facts: tuple[str, ...] = ()) -> AuthorizationDecision:
        return self._record(AuthorizationDecision(str(uuid4()), AuthorizationEffect.DENY, reason, roles, grants, (self._policy_version,), obligations, missing_facts, self._clock()))

    def evaluate(self, request: AuthorizationRequest) -> AuthorizationDecision:
        action = self._actions.get(request.action)
        if action is None:
            return self._deny("unknown_action")
        if request.principal.tenant_id != request.resource.tenant_id:
            return self._deny("cross_tenant")
        if action.resource_type != request.resource.resource_type:
            return self._deny("resource_type_mismatch")
        if action.required_acr and request.authentication.acr != action.required_acr:
            return self._deny("assurance_insufficient", obligations=("step_up",))
        if request.principal.attributes.get("status") == "suspended":
            return self._deny("principal_suspended")
        now = self._clock()
        applicable = [g for g in self._grants if g.principal.principal_id == request.principal.principal_id and g.tenant_id == request.resource.tenant_id and g.resource.resource_type == request.resource.resource_type and g.resource.resource_id in (request.resource.resource_id, "*")]
        expired = [g for g in applicable if g.expires_at and g.expires_at <= now]
        revoked = [g for g in applicable if g.revoked_at is not None]
        active = [g for g in applicable if g.revoked_at is None and (not g.valid_from or g.valid_from <= now) and (not g.expires_at or g.expires_at > now)]
        matches: list[tuple[RoleGrant, RoleDefinition]] = []
        for grant in active:
            role = self._roles.get(grant.role_id)
            if not role or request.action not in role.actions:
                continue
            facts = {**request.principal.attributes, **request.resource.attributes, **request.environment}
            missing = tuple(sorted(key for key in grant.conditions if key not in facts))
            if missing:
                return self._deny("missing_fact", grants=(grant.grant_id,), roles=(role.role_id,), missing_facts=missing)
            if all(facts[key] == value for key, value in grant.conditions.items()):
                matches.append((grant, role))
        denied = [(grant, role) for grant, role in matches if grant.effect is AuthorizationEffect.DENY]
        if denied:
            return self._deny("explicit_deny", grants=tuple(grant.grant_id for grant, _ in denied), roles=tuple(role.role_id for _, role in denied))
        if matches:
            return self._record(AuthorizationDecision(str(uuid4()), AuthorizationEffect.ALLOW, "matching_grant", tuple(role.role_id for _, role in matches), tuple(grant.grant_id for grant, _ in matches), (self._policy_version,), evaluated_at=now))
        if revoked:
            return self._deny("grant_revoked", grants=tuple(g.grant_id for g in revoked))
        if expired:
            return self._deny("grant_expired", grants=tuple(g.grant_id for g in expired))
        return self._deny("no_matching_grant")

    def evaluate_batch(self, requests: Iterable[AuthorizationRequest]) -> tuple[AuthorizationDecision, ...]:
        return tuple(self.evaluate(request) for request in requests)

    def simulate(self, request: AuthorizationRequest, *, grants: Iterable[RoleGrant]) -> AuthorizationDecision:
        simulation = PlatformPolicyDecisionEngine(actions=self._actions.values(), roles=self._roles.values(), grants=grants, policy_version=f"{self._policy_version}:simulation", clock=self._clock)
        return simulation.evaluate(request)
