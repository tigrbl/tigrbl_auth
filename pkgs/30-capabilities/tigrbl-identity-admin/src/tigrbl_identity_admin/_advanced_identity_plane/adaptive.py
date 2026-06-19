from __future__ import annotations

from .models import AdaptiveContext, AdaptiveDecision


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
        return AdaptiveDecision(
            allowed=False,
            step_up_required=True,
            risk_level="high",
            reasons=tuple(reasons or ("bounded contextual risk threshold exceeded",)),
            amr=("mfa", "rba"),
        )
    if risk_score >= 2:
        return AdaptiveDecision(
            allowed=True,
            step_up_required=True,
            risk_level="medium",
            reasons=tuple(reasons or ("adaptive step-up required",)),
            amr=("mfa", "rba"),
        )
    return AdaptiveDecision(
        allowed=True,
        step_up_required=False,
        risk_level="low",
        reasons=tuple(reasons or ("context accepted within bounded policy",)),
        amr=("pwd",),
    )
