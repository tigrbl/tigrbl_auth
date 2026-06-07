from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_auth.services.formal_authorization import PolicyReplayCase as FacadePolicyReplayCase
from tigrbl_identity_policy import PolicyReplayCase, replay_policy_determinism


def test_policy_determinism_replay_t0_exports_facade_identity() -> None:
    assert FacadePolicyReplayCase is PolicyReplayCase


def test_policy_determinism_replay_t1_accepts_stable_decisions() -> None:
    report = replay_policy_determinism(
        policy_version="policy:v1",
        cases=(PolicyReplayCase("case:read", {"subject": "alice", "action": "client.read"}),),
        evaluator=lambda request: {
            "allowed": request["action"] == "client.read",
            "reason": "static policy",
        },
        runs=3,
    )

    assert report.passed is True
    assert report.results[0].stable is True
    assert len(set(report.results[0].decision_hashes)) == 1


def test_policy_determinism_replay_t1_rejects_unstable_decisions() -> None:
    counter = {"value": 0}

    def evaluator(_request: dict[str, str]) -> dict[str, int]:
        counter["value"] += 1
        return {"counter": counter["value"]}

    report = replay_policy_determinism(
        policy_version="policy:v1",
        cases=(PolicyReplayCase("case:counter", {"subject": "alice"}),),
        evaluator=evaluator,
    )

    assert report.passed is False
    assert report.failures == ("case 'case:counter' produced non-deterministic decisions",)
