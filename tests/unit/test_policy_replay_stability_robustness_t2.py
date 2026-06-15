from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import (
    PolicyReplayCase,
    canonical_hash,
    compare_policy_version_decisions,
    replay_policy_determinism,
)


def test_policy_replay_t2_canonical_ordering_and_decision_hashes_are_stable() -> None:
    case_a = PolicyReplayCase("case:ordered", {"roles": ["admin", "viewer"], "attrs": {"b": 2, "a": 1}})
    case_b = PolicyReplayCase("case:ordered", {"attrs": {"a": 1, "b": 2}, "roles": ["admin", "viewer"]})

    report_a = replay_policy_determinism(
        policy_version="policy:v1",
        schema_version="schema:v1",
        cases=(case_a,),
        evaluator=lambda request: {"allowed": True, "request_hash": canonical_hash(request)},
        runs=3,
    )
    report_b = replay_policy_determinism(
        policy_version="policy:v1",
        schema_version="schema:v1",
        cases=(case_b,),
        evaluator=lambda request: {"allowed": True, "request_hash": canonical_hash(request)},
        runs=3,
    )

    assert report_a.passed is True
    assert report_a.schema_version == "schema:v1"
    assert report_a.results[0].request_hash == report_b.results[0].request_hash
    assert report_a.results[0].decision_hashes == report_b.results[0].decision_hashes


def test_policy_replay_t2_detects_time_random_or_environment_style_decision_dependency() -> None:
    counter = {"value": 0}

    def evaluator(_request: dict[str, str]) -> dict[str, int]:
        counter["value"] += 1
        return {"allowed": True, "ambient_counter": counter["value"]}

    report = replay_policy_determinism(
        policy_version="policy:v1",
        cases=(PolicyReplayCase("case:ambient", {"action": "client.read"}),),
        evaluator=evaluator,
        runs=3,
    )

    assert report.passed is False
    assert report.failures == ("case 'case:ambient' produced non-deterministic decisions",)


def test_policy_replay_t2_covers_allow_and_deny_corpus() -> None:
    report = replay_policy_determinism(
        policy_version="policy:v1",
        cases=(
            PolicyReplayCase("case:allow", {"action": "client.read"}),
            PolicyReplayCase("case:deny", {"action": "client.delete"}),
        ),
        evaluator=lambda request: {"allowed": request["action"] == "client.read"},
        runs=2,
    )

    assert report.passed is True
    assert tuple(result.decisions[0]["allowed"] for result in report.results) == (True, False)


def test_policy_version_stability_t2_requires_attribution_for_allow_to_deny_and_deny_to_allow_and_records_versions() -> None:
    allow_to_deny = compare_policy_version_decisions(
        baseline_version="policy:v1",
        candidate_version="policy:v1",
        baseline_schema_version="schema:v1",
        candidate_schema_version="schema:v1",
        cases=(PolicyReplayCase("case:allow-deny", {"action": "client.read"}),),
        baseline_evaluator=lambda _request: {"allowed": True},
        candidate_evaluator=lambda _request: {"allowed": False},
    )
    deny_to_allow = compare_policy_version_decisions(
        baseline_version="policy:v1",
        candidate_version="policy:v1",
        cases=(PolicyReplayCase("case:deny-allow", {"action": "client.delete"}),),
        baseline_evaluator=lambda _request: {"allowed": False},
        candidate_evaluator=lambda _request: {"allowed": True},
    )
    attributed = compare_policy_version_decisions(
        baseline_version="policy:v1",
        candidate_version="policy:v2",
        baseline_schema_version="schema:v1",
        candidate_schema_version="schema:v2",
        cases=(PolicyReplayCase("case:delete", {"action": "client.delete"}),),
        baseline_evaluator=lambda _request: {"allowed": False},
        candidate_evaluator=lambda _request: {"allowed": True},
        allowed_change_reasons={"case:delete": "policy:v2/schema:v2 adds delegated delete"},
    )

    assert allow_to_deny.passed is False
    assert deny_to_allow.passed is False
    assert attributed.passed is True
    assert attributed.baseline_schema_version == "schema:v1"
    assert attributed.candidate_schema_version == "schema:v2"


def test_policy_version_stability_t2_detects_unattributed_version_downgrade_instability() -> None:
    report = compare_policy_version_decisions(
        baseline_version="policy:v2",
        candidate_version="policy:v1",
        cases=(PolicyReplayCase("case:downgrade", {"action": "client.write"}),),
        baseline_evaluator=lambda _request: {"allowed": True},
        candidate_evaluator=lambda _request: {"allowed": False},
    )

    assert report.passed is False
    assert report.failures == ("case 'case:downgrade' changed without policy-version attribution",)
