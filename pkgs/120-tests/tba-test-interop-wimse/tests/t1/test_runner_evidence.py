from dataclasses import replace
from contextlib import contextmanager

import pytest

from tba_test_interop_wimse.adapters import REFERENCE_ADAPTERS
from tba_test_interop_wimse.evidence import reconcile
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.observations import Observation, mismatches
from tba_test_interop_wimse.runner import run_inventory


def test_release_and_revocation_reference_effects():
    cases = [row for row in generate_matrix()["scenarios"] if row["scenario_id"] in {"12", "18"}]
    runs = [{"id": row["id"], "scenario_id": row["id"], "status": "qualified"} for row in cases]
    results = list(run_inventory(cases, runs, REFERENCE_ADAPTERS))
    assert len(results) == len(cases)
    assert {row["status"] for row in results} == {"passed"}


def test_denial_cannot_pass_with_effect_or_wrong_order():
    case = {"scenario_id": "12", "target_hop": "enforcing", "decision": "deny",
            "effect": "zero-effects",
            "events": ["initial-allow", "revocation-observed", "commit-refused"]}
    observed = Observation("deny", "enforcing", tuple(case["events"]))
    assert not mismatches(case, observed)
    assert mismatches(case, replace(observed, effects=1))
    assert mismatches(case, replace(observed, events=observed.events[::-1]))


def test_failed_control_blocks_batch_and_preserves_attempts():
    class Failing:
        supports = lambda self, case: True
        setup_key = lambda self, case, run: "same"

        def check_setup(self, case, run):
            raise ValueError("baseline unavailable")

        @contextmanager
        def isolated(self, case, run):
            pytest.fail("failed setup must never run a case")
            yield

    case = {"id": "s", "scenario_id": "12"}
    rows = [{"id": key, "scenario_id": "s", "status": "qualified"} for key in ("a", "b")]
    results = list(run_inventory([case], rows, {"12": Failing()}))
    assert [r["status"] for r in results] == ["setup-failure", "setup-failure"]
    first = dict(results[0], attempt=1)
    rerun = dict(first, status="passed", attempt=2)
    report = reconcile(["a", "b"], [rerun, first])
    assert report["a"]["attempts"] == [first, rerun]
    assert report["b"]["status"] == "not-run"
    with pytest.raises(ValueError, match="duplicate"):
        reconcile(["a"], [first, first])
