"""Stateful policy decision provider over deterministic layer-10 evaluation."""

from __future__ import annotations

from tigrbl_identity_contracts.policy.decisions import PolicyDecision, PolicyTrace
from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_policy_decision_engine_default import (
    AdminPolicy,
    AttributePolicy,
    DecisionEffect,
    DelegationPolicy,
    PermissionPolicy,
    PolicyDecisionEvaluator,
    PolicyKind,
    PolicyRequest,
    RolePolicy,
)


class PolicyDecisionEngine:
    """Evaluate policy deterministically and retain provider-owned decision traces."""

    def __init__(self, **policy_sets: object) -> None:
        self._evaluator = PolicyDecisionEvaluator(**policy_sets)
        self._traces: list[PolicyTrace] = []

    @property
    def traces(self) -> tuple[PolicyTrace, ...]:
        return tuple(self._traces)

    def decide_rbac(self, request: PolicyRequest) -> PolicyDecision:
        return self._evaluator.decide_rbac(request)

    def decide_abac(self, request: PolicyRequest) -> PolicyDecision:
        return self._evaluator.decide_abac(request)

    def decide_pbac(self, request: PolicyRequest) -> PolicyDecision:
        return self._evaluator.decide_pbac(request)

    def decide_delegation(self, request: PolicyRequest) -> PolicyDecision:
        return self._evaluator.decide_delegation(request)

    def decide_admin(self, request: PolicyRequest) -> PolicyDecision:
        return self._evaluator.decide_admin(request)

    def evaluate(self, request: PolicyRequest) -> PolicyDecision:
        decision = self._evaluator.evaluate(request)
        trace_id = f"poltrace:{len(self._traces) + 1}"
        self._traces.append(
            PolicyTrace(
                trace_id=trace_id,
                subject=request.subject,
                tenant_id=request.tenant_id,
                action=request.action,
                allowed=decision.allowed,
                reason=decision.reason,
                matched=decision.matched,
                evaluated_kinds=(
                    PolicyKind.DELEGATION,
                    PolicyKind.ADMIN,
                    PolicyKind.RBAC,
                    PolicyKind.ABAC,
                    PolicyKind.PBAC,
                ),
                recorded_at=utc_now_iso(),
            )
        )
        return PolicyDecision(
            decision.allowed,
            decision.reason,
            decision.matched,
            trace_id,
        )


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
