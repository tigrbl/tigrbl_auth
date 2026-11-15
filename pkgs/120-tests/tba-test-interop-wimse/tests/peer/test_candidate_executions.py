"""Collect one independently reportable pytest item per peer execution."""

import json
import os
from pathlib import Path

import pytest

from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.runner import run_inventory


def pytest_generate_tests(metafunc):
    if "candidate" not in metafunc.fixturenames:
        return
    snapshot = os.getenv("TBA_WIMSE_PEER_SNAPSHOT")
    peers = json.loads(Path(snapshot).read_text(encoding="utf-8"))["peers"] if snapshot else None
    matrix = generate_matrix(peers=peers)
    if peers is not None:
        def candidate_key(row):
            return row["scenario_id"], tuple(
                (pair["caller"]["implementation"], pair["receiver"]["implementation"])
                for pair in row["pairs"].values()
            )

        original = {candidate_key(row) for row in generate_matrix()["executions"]}
        current = {candidate_key(row) for row in matrix["executions"]}
        if original != current or len(matrix["executions"]) != len(original):
            raise ValueError("Qualification snapshot changed the candidate inventory")
    cases = {row["id"]: row for row in matrix["scenarios"]}
    metafunc.parametrize(
        "candidate",
        [
            pytest.param((cases[row["scenario_id"]], row), id=row["id"])
            for row in matrix["executions"]
        ],
    )


def test_peer_execution(candidate, request, peer_setup_cache, record_property):
    case, execution = candidate
    adapters = {}
    if execution["status"] == "qualified":
        if any(endpoint["implementation"] == "cred" and endpoint["profile"] == "wit-http-signature"
               for pair in execution["pairs"].values() for endpoint in pair.values()):
            adapter = request.getfixturevalue("cred_http_signature_adapter")
            adapters = dict.fromkeys(adapter.families, adapter)
        else:
            adapters = request.getfixturevalue("peer_adapters")
    result, = run_inventory(
        [case], [execution], adapters, setup_cache=peer_setup_cache
    )
    record_property("execution_id", execution["id"])
    record_property("scenario_id", case["id"])
    record_property("execution_result", json.dumps(result, sort_keys=True))
    if result["status"] == "blocked":
        pytest.skip(result["reason"])
    assert result["status"] == "passed", result
