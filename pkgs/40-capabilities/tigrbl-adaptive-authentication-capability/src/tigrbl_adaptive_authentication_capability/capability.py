"""Adaptive-authentication decision capability."""

from __future__ import annotations

from collections.abc import Callable

from tigrbl_capability import Capability
from tigrbl_identity_contracts.adaptive_access import AdaptiveContext, AdaptiveDecision
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation

AdaptiveEvaluator = Callable[[AdaptiveContext], AdaptiveDecision]


def evaluate_adaptive_context(context: AdaptiveContext) -> AdaptiveDecision:
    reasons: list[str] = []
    risk_score = 0
    if not context.trusted_network:
        risk_score += 1
        reasons.append("untrusted network context")
    if not context.trusted_device:
        risk_score += 2
        reasons.append("unknown or unhealthy device posture")
    if context.local_hour < 6 or context.local_hour > 22:
        risk_score += 1
        reasons.append("outside normal operating hours")
    if context.known_countries and context.ip_country not in context.known_countries:
        risk_score += 2
        reasons.append("unrecognized location")
    if context.anomaly_detected:
        risk_score += 2
        reasons.append("upstream anomaly signal present")
    if risk_score >= 5:
        return AdaptiveDecision(False, True, "high", tuple(reasons or ("bounded contextual risk threshold exceeded",)), ("mfa", "rba"))
    if risk_score >= 2:
        return AdaptiveDecision(True, True, "medium", tuple(reasons or ("adaptive step-up required",)), ("mfa", "rba"))
    return AdaptiveDecision(True, False, "low", tuple(reasons or ("context accepted within bounded policy",)), ("pwd",))


class AdaptiveAuthenticationCapability(Capability):
    def __init__(self, evaluator: AdaptiveEvaluator = evaluate_adaptive_context) -> None:
        self._evaluator = evaluator
        super().__init__(CapabilityDefinition("authentication.adaptive", "1.0"), operations={"evaluate_adaptive_context": CapabilityOperation(target=self.evaluate_adaptive_context, delegated=True)})

    def evaluate_adaptive_context(self, context: AdaptiveContext) -> AdaptiveDecision:
        return self._evaluator(context)


__all__ = ["AdaptiveAuthenticationCapability", "AdaptiveEvaluator", "evaluate_adaptive_context"]
