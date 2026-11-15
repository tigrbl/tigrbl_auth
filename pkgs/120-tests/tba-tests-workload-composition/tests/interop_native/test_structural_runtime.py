"""Native execution inventory with an explicit result per structural ID."""

import json

import pytest

from tba_tests_interop_wimse.matrix import generate_matrix
from tba_tests_interop_wimse.runner import run_inventory

from support.wic_fixture import NativeWicAdapter
from support.wpt_fixture import NativeWptAdapter


@pytest.fixture(scope="module")
def native_bindings(tmp_path_factory):
    directory = tmp_path_factory.mktemp("native-matrix")
    return (NativeWicAdapter(directory), NativeWptAdapter(directory)), {}


@pytest.mark.parametrize("case", generate_matrix()["scenarios"], ids=lambda case: case["id"])
def test_structural_runtime(case, native_bindings, record_property):
    adapters, cache = native_bindings
    binding = next((adapter for adapter in adapters if adapter.supports(case)), None)
    execution = {"id": case["id"], "scenario_id": case["id"], "status": "qualified"}
    result, = run_inventory([case], [execution], {case["scenario_id"]: binding}, setup_cache=cache)
    record_property("execution_result", json.dumps(result, sort_keys=True))
    if result["status"] == "blocked":
        pytest.skip(result["reason"])
    assert result["status"] == "passed", result
