from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import PolicyReplayCase, compare_policy_version_decisions


def test_decision_stability_policy_versions_t1_attributes_version_changes() -> None:
    case = PolicyReplayCase("case:delete", {"subject": "alice", "action": "client.delete"})

    report = compare_policy_version_decisions(
        baseline_version="policy:v1",
        candidate_version="policy:v2",
        cases=(case,),
        baseline_evaluator=lambda _request: {"allowed": False, "reason": "not granted"},
        candidate_evaluator=lambda _request: {"allowed": True, "reason": "policy v2 grant"},
        allowed_change_reasons={"case:delete": "policy:v2 added client.delete for tenant admins"},
    )

    assert report.passed is True
    assert report.changes[0].attributed is True
    assert "policy:v2" in report.changes[0].reason


def test_decision_stability_policy_versions_t1_rejects_unattributed_changes() -> None:
    report = compare_policy_version_decisions(
        baseline_version="policy:v1",
        candidate_version="policy:v1",
        cases=(PolicyReplayCase("case:read", {"action": "client.read"}),),
        baseline_evaluator=lambda _request: {"allowed": True},
        candidate_evaluator=lambda _request: {"allowed": False},
    )

    assert report.passed is False
    assert report.failures == ("case 'case:read' changed without policy-version attribution",)
