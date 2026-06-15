from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import (
    AuthorizationInvariant,
    AuthorizationSafetyPropertyEvaluator,
    InvariantEvaluation,
    InvariantRegistry,
    VerificationMethod,
)


def test_authorization_safety_property_evaluator_t1_reports_invariant_failures() -> None:
    registry = InvariantRegistry(
        (
            AuthorizationInvariant(
                invariant_id="authz.no_escalation",
                title="No escalation",
                property_family="safety",
                statement="Authority cannot exceed granted closure.",
                verification_method=VerificationMethod.GRAPH,
            ),
        )
    )

    result = AuthorizationSafetyPropertyEvaluator(registry).evaluate(
        (
            InvariantEvaluation(
                invariant_id="authz.no_escalation",
                passed=False,
                message="effective authority exceeded closure",
                evaluated_at="2026-06-07T00:00:00+00:00",
            ),
        )
    )

    assert result.passed is False
    assert result.failures == ("effective authority exceeded closure",)
