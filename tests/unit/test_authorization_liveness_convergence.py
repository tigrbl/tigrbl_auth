from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import ConvergenceEvent, ConvergenceState, evaluate_liveness_convergence


def test_authorization_liveness_convergence_t1_classifies_converged_pending_and_late() -> None:
    report = evaluate_liveness_convergence(
        (
            ConvergenceEvent(
                "evt:1",
                "mutation:revoke",
                "delegation:1",
                issued_at="2026-06-07T00:00:00+00:00",
                observed_at="2026-06-07T00:00:10+00:00",
                expected_within_seconds=30,
            ),
            ConvergenceEvent(
                "evt:2",
                "mutation:rotate",
                "key:1",
                issued_at="2026-06-07T00:00:00+00:00",
                observed_at="2026-06-07T00:02:00+00:00",
                expected_within_seconds=30,
            ),
            ConvergenceEvent(
                "evt:3",
                "mutation:policy",
                "policy:1",
                issued_at="2026-06-07T00:00:00+00:00",
            ),
        )
    )

    assert report.passed is False
    assert report.converged[0].state is ConvergenceState.CONVERGED
    assert tuple(event.mutation_id for event in report.pending) == ("mutation:policy",)
    assert tuple(event.mutation_id for event in report.late) == ("mutation:rotate",)
