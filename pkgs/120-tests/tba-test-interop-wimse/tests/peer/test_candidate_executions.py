"""Collect one independently reportable pytest item per peer execution."""

import json

import pytest

from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.runner import run_inventory


def pytest_generate_tests(metafunc):
    if "candidate" not in metafunc.fixturenames:
        return
    matrix = generate_matrix()
    cases = {row["id"]: row for row in matrix["scenarios"]}
    metafunc.parametrize(
        "candidate",
        [
            pytest.param((cases[row["scenario_id"]], row), id=row["id"])
            for row in matrix["executions"]
        ],
    )


def test_peer_execution(candidate, peer_adapters, peer_setup_cache, record_property):
    case, execution = candidate
    result, = run_inventory(
        [case], [execution], peer_adapters, setup_cache=peer_setup_cache
    )
    record_property("execution_id", execution["id"])
    record_property("scenario_id", case["id"])
    record_property("execution_result", json.dumps(result, sort_keys=True))
    if result["status"] == "blocked":
        pytest.skip(result["reason"])
    assert result["status"] == "passed", result
