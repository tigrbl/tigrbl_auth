from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from tigrbl_identity_contracts.policy.decisions import PolicyDecision, PolicyTrace
from tigrbl_identity_contracts.policy.effects import DecisionEffect
from tigrbl_identity_contracts.policy.kinds import PolicyKind
from tigrbl_identity_contracts.policy.requests import PolicyRequest
from tigrbl_authz_policy_concrete import (
    AdminPolicy,
    AttributePolicy,
    DelegationPolicy,
    PermissionPolicy,
    RolePolicy,
)


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _matches(pattern: str, value: str) -> bool:
    if pattern == "*" or pattern == value:
        return True
    if pattern.endswith(".*"):
        prefix = pattern[:-2]
        return value == prefix or value.startswith(f"{prefix}.")
    return False


class PolicyDecisionEngine:
    def __init__(
        self,
        *,
        roles: Iterable[RolePolicy] = (),
        attributes: Iterable[AttributePolicy] = (),
        permissions: Iterable[PermissionPolicy] = (),
        delegations: Iterable[DelegationPolicy] = (),
        admins: Iterable[AdminPolicy] = (),
    ) -> None:
        self.roles = tuple(roles)
        self.attributes = tuple(attributes)
        self.permissions = tuple(permissions)
        self.delegations = tuple(delegations)
        self.admins = tuple(admins)
        self._traces: list[PolicyTrace] = []

    @property
    def traces(self) -> tuple[PolicyTrace, ...]:
        return tuple(self._traces)

    def decide_rbac(self, request: PolicyRequest) -> PolicyDecision:
        matched_allow: list[str] = []
        matched_deny: list[str] = []
        for policy in self.roles:
            if policy.tenant_id not in {None, request.tenant_id}:
                continue
            if policy.role not in request.roles:
                continue
            if any(_matches(permission, request.action) for permission in policy.permissions):
                if policy.effect == DecisionEffect.DENY:
                    matched_deny.append(policy.role)
                else:
                    matched_allow.append(policy.role)
        if matched_deny:
            return PolicyDecision(False, "denied by RBAC role policy", tuple(sorted(matched_deny)))
        if matched_allow:
            return PolicyDecision(True, "allowed by RBAC role policy", tuple(sorted(matched_allow)))
        return PolicyDecision(False, "no RBAC role policy matched", ())

    def decide_abac(self, request: PolicyRequest) -> PolicyDecision:
        matched_allow: list[str] = []
        matched_deny: list[str] = []
        for policy in self.attributes:
            if policy.tenant_id not in {None, request.tenant_id}:
                continue
            if not _matches(policy.action, request.action):
                continue
            if not all(request.attributes.get(key) == value for key, value in policy.required_attributes.items()):
                continue
            if policy.effect == DecisionEffect.DENY:
                matched_deny.append(policy.policy_id)
            else:
                matched_allow.append(policy.policy_id)
        if matched_deny:
            return PolicyDecision(False, "denied by ABAC attribute policy", tuple(sorted(matched_deny)))
        if matched_allow:
            return PolicyDecision(True, "allowed by ABAC attribute policy", tuple(sorted(matched_allow)))
        return PolicyDecision(False, "no ABAC attribute policy matched", ())

    def decide_pbac(self, request: PolicyRequest) -> PolicyDecision:
        matched_allow: list[str] = []
        matched_deny: list[str] = []
        granted = set(request.permissions)
        for policy in self.permissions:
            if policy.tenant_id not in {None, request.tenant_id}:
                continue
            if not any(_matches(permission, request.action) for permission in policy.permissions):
                continue
            if not granted.intersection(policy.permissions) and "*" not in granted:
                continue
            if policy.effect == DecisionEffect.DENY:
                matched_deny.append(policy.policy_id)
            else:
                matched_allow.append(policy.policy_id)
        if matched_deny:
            return PolicyDecision(False, "denied by PBAC permission policy", tuple(sorted(matched_deny)))
        if matched_allow:
            return PolicyDecision(True, "allowed by PBAC permission policy", tuple(sorted(matched_allow)))
        return PolicyDecision(False, "no PBAC permission policy matched", ())

    def decide_delegation(self, request: PolicyRequest) -> PolicyDecision:
        if request.delegated_by is None:
            return PolicyDecision(True, "no delegation constraint active", ())
        for policy in self.delegations:
            if policy.delegate != request.subject or policy.delegator != request.delegated_by:
                continue
            if request.tenant_id not in policy.tenant_ids:
                return PolicyDecision(False, "delegation tenant scope denied", (policy.delegator,))
            if any(_matches(action, request.action) for action in policy.actions):
                return PolicyDecision(True, "allowed by delegation policy", (policy.delegator,))
        return PolicyDecision(False, "no delegation policy matched", ())

    def decide_admin(self, request: PolicyRequest) -> PolicyDecision:
        if not request.admin:
            return PolicyDecision(True, "no admin policy required", ())
        for policy in self.admins:
            if policy.subject != request.subject:
                continue
            if policy.superuser:
                return PolicyDecision(True, "allowed by superuser admin policy", (policy.subject,))
            if request.tenant_id in policy.tenant_ids and any(_matches(action, request.action) for action in policy.actions):
                return PolicyDecision(True, "allowed by tenant admin policy", (policy.subject,))
        return PolicyDecision(False, "admin policy denied", ())

    def evaluate(self, request: PolicyRequest) -> PolicyDecision:
        decisions = (
            (PolicyKind.DELEGATION, self.decide_delegation(request)),
            (PolicyKind.ADMIN, self.decide_admin(request)),
            (PolicyKind.RBAC, self.decide_rbac(request)),
            (PolicyKind.ABAC, self.decide_abac(request)),
            (PolicyKind.PBAC, self.decide_pbac(request)),
        )
        hard_denies = [
            (kind, decision)
            for kind, decision in decisions
            if not decision.allowed and kind in {PolicyKind.DELEGATION, PolicyKind.ADMIN}
        ]
        allow_decisions = [
            (kind, decision)
            for kind, decision in decisions
            if decision.allowed and kind in {PolicyKind.RBAC, PolicyKind.ABAC, PolicyKind.PBAC}
        ]
        if hard_denies:
            allowed = False
            reason = hard_denies[0][1].reason
        elif allow_decisions:
            allowed = True
            reason = "allowed by policy decision engine"
        else:
            allowed = False
            reason = "no granting policy matched"
        matched = tuple(sorted({item for _kind, decision in decisions for item in decision.matched}))
        trace_id = f"poltrace:{len(self._traces) + 1}"
        trace = PolicyTrace(
            trace_id=trace_id,
            subject=request.subject,
            tenant_id=request.tenant_id,
            action=request.action,
            allowed=allowed,
            reason=reason,
            matched=matched,
            evaluated_kinds=tuple(kind for kind, _decision in decisions),
            recorded_at=_utc_now(),
        )
        self._traces.append(trace)
        return PolicyDecision(allowed, reason, matched, trace_id)


__all__ = [
    "AdminPolicy",
    "AttributePolicy",
    "DecisionEffect",
    "DelegationPolicy",
    "PermissionPolicy",
    "PolicyDecision",
    "PolicyDecisionEngine",
    "PolicyKind",
    "PolicyRequest",
    "PolicyTrace",
    "RolePolicy",
]
