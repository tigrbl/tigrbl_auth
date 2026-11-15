"""Collect one independently reportable pytest item per peer execution."""

import json
import os
from pathlib import Path
from functools import lru_cache

import pytest

from tba_test_interop_wimse.hop_runner import run_hop_execution
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.native_expansion import (
    COMBINED_SCOPE, NATIVE_ISSUERS, expanded_plan, native_baseline_workload_rows, native_issuer_rows,
)
from tba_test_interop_wimse.runner import run_inventory
from external_workload_selection import endpoint_candidates, spiffe_peer_rows, spiffe_support_rows
from typed_service_selection import (
    acquisition_control_rows, native_acquisition_rows, native_baseline_policy_rows, service_control_rows,
    native_svid_policy_rows, svid_policy_control_rows, typed_service_rows,
)

EXPANDED = os.getenv("TBA_WIMSE_EXPANDED") == "1"
NATIVE = os.getenv("TBA_WIMSE_INCLUDE_NATIVE") == "1"
TYPED_SERVICE = os.getenv("TBA_WIMSE_TYPED_SERVICE") == "1"
SPIFFE_PEER_RUN = os.getenv("TBA_WIMSE_GO_SPIFFE_ONLY")
SPIFFE_SUPPORT = {"emilia": "emilia", "teleport": "teleport-tbot", "mintid": "mintid"}.get(SPIFFE_PEER_RUN)
ACQUISITION_MODE = os.getenv("TBA_WIMSE_NATIVE_ACQUISITION")
NATIVE_ACQUISITION = ACQUISITION_MODE in {"1", "specialized"}
NATIVE_BASELINE_WORKLOAD = os.getenv("TBA_WIMSE_NATIVE_BASELINE_WORKLOAD") == "1"
NATIVE_POLICY_MODE = os.getenv("TBA_WIMSE_NATIVE_BASELINE_POLICY")
NATIVE_POLICY = NATIVE_POLICY_MODE in {"1", "svid"}
NATIVE_ISSUER = os.getenv("TBA_WIMSE_NATIVE_ISSUER")
if not NATIVE_ISSUER and os.getenv("TBA_WIMSE_NATIVE_WIT_ONLY") == "1":
    NATIVE_ISSUER = "tba-wit-svid"
SELECTED_ID = os.getenv("TBA_WIMSE_EXECUTION_ID")
SELECTED_TYPED_ID = bool(SELECTED_ID and SELECTED_ID.startswith("hop-v1:"))
HOP_PATH_FILTER = os.getenv("TBA_WIMSE_HOP_PATH")
HOP_PATH = tuple(part.strip() for part in HOP_PATH_FILTER.split(",")) if HOP_PATH_FILTER else ()
if NATIVE and not EXPANDED:
    raise pytest.UsageError("TBA_WIMSE_INCLUDE_NATIVE requires TBA_WIMSE_EXPANDED=1")
if SPIFFE_PEER_RUN and (not EXPANDED or NATIVE or TYPED_SERVICE
                       or SPIFFE_PEER_RUN not in {"1", "defakto", "emilia", "teleport", "mintid"}):
    raise pytest.UsageError("SPIFFE peer selection requires an expanded external workload run")
if TYPED_SERVICE and not NATIVE:
    raise pytest.UsageError("TBA_WIMSE_TYPED_SERVICE requires expanded native collection")
if NATIVE_ACQUISITION and (not NATIVE or TYPED_SERVICE or NATIVE_ISSUER):
    raise pytest.UsageError("TBA_WIMSE_NATIVE_ACQUISITION requires an exclusive expanded native selection")
if NATIVE_BASELINE_WORKLOAD and (
    not NATIVE or TYPED_SERVICE or NATIVE_ISSUER or NATIVE_ACQUISITION or NATIVE_POLICY
    or HOP_PATH or SELECTED_TYPED_ID
):
    raise pytest.UsageError("TBA_WIMSE_NATIVE_BASELINE_WORKLOAD requires an exclusive expanded workload selection")
if NATIVE_POLICY and (not NATIVE or TYPED_SERVICE or NATIVE_ISSUER or NATIVE_ACQUISITION):
    raise pytest.UsageError("Native policy selection requires an exclusive expanded native selection")
if NATIVE_ISSUER and (NATIVE_ISSUER not in {*NATIVE_ISSUERS, COMBINED_SCOPE} or not NATIVE):
    raise pytest.UsageError("A native issuer selection requires a known issuer and TBA_WIMSE_INCLUDE_NATIVE=1")
if HOP_PATH and SELECTED_ID and not SELECTED_TYPED_ID:
    raise pytest.UsageError("A workload execution ID cannot be combined with TBA_WIMSE_HOP_PATH")


@lru_cache(maxsize=1)
def execution_inventory():
    snapshot = os.getenv("TBA_WIMSE_PEER_SNAPSHOT")
    if (SELECTED_TYPED_ID or HOP_PATH) and not EXPANDED:
        raise pytest.UsageError("Selecting typed hops requires TBA_WIMSE_EXPANDED=1")
    if EXPANDED and not snapshot:
        raise pytest.UsageError("TBA_WIMSE_EXPANDED=1 requires TBA_WIMSE_PEER_SNAPSHOT")
    peers = json.loads(Path(snapshot).read_text(encoding="utf-8"))["peers"] if snapshot else None
    matrix = generate_matrix(peers=peers)
    if peers is not None and SPIFFE_PEER_RUN not in {"teleport", "mintid"}:
        def candidate_key(row):
            return row["scenario_id"], tuple(
                (pair["caller"]["implementation"], pair["receiver"]["implementation"])
                for pair in row["pairs"].values()
            )

        original = {candidate_key(row) for row in generate_matrix()["executions"]}
        current = {candidate_key(row) for row in matrix["executions"]}
        if not original <= current or (not EXPANDED and (
            original != current or len(matrix["executions"]) != len(original)
        )):
            raise ValueError("Qualification snapshot changed the candidate inventory")
    if EXPANDED:
        plan = expanded_plan(peers, include_candidates=True, include_native=NATIVE, include_executions=True)
        if SPIFFE_SUPPORT:
            plan["workload_executions"] = []
            plan["planned_executions"] = spiffe_support_rows(plan, SPIFFE_SUPPORT)
        elif SPIFFE_PEER_RUN:
            plan["workload_executions"], plan["planned_executions"] = spiffe_peer_rows(
                plan, defakto=SPIFFE_PEER_RUN == "defakto",
            )
        elif NATIVE_BASELINE_WORKLOAD:
            plan["workload_executions"] = native_baseline_workload_rows(plan)
        elif NATIVE_POLICY:
            if NATIVE_POLICY_MODE == "svid":
                rows, controls = native_svid_policy_rows(plan), svid_policy_control_rows
            else:
                rows, controls = native_baseline_policy_rows(plan), service_control_rows
            plan["planned_executions"] = controls(rows) if os.getenv("TBA_WIMSE_SERVICE_CONTROLS") == "1" else rows
        elif NATIVE_ISSUER:
            plan["workload_executions"], plan["planned_executions"] = native_issuer_rows(plan, NATIVE_ISSUER)
        elif NATIVE_ACQUISITION:
            specialized = ACQUISITION_MODE == "specialized"
            rows = native_acquisition_rows(plan, specialized=specialized)
            plan["planned_executions"] = (
                acquisition_control_rows(rows, specialized=specialized)
                if os.getenv("TBA_WIMSE_SERVICE_CONTROLS") == "1" else rows
            )
        elif TYPED_SERVICE:
            service_rows = typed_service_rows(plan)
            plan["planned_executions"] = (
                service_control_rows(service_rows) if os.getenv("TBA_WIMSE_SERVICE_CONTROLS") == "1" else service_rows
            )
        return plan
    return {"scenario_definitions": matrix["scenarios"], "workload_executions": matrix["executions"]}


def pytest_generate_tests(metafunc):
    typed = "hop_execution" in metafunc.fixturenames
    if not typed and "candidate" not in metafunc.fixturenames:
        return
    inventory = execution_inventory()
    if typed:
        rows = inventory["planned_executions"]
        if HOP_PATH:
            rows = [row for row in rows if tuple(hop["operation"] for hop in row["hops"]) == HOP_PATH]
            if not rows:
                raise pytest.UsageError(f"No typed executions for path: {HOP_PATH}")
        rows = select_executions(rows, SELECTED_ID)
        metafunc.parametrize("hop_execution", [pytest.param(row, id=row["id"]) for row in rows])
        return
    cases = {row["id"]: row for row in inventory["scenario_definitions"]}
    rows = inventory["workload_executions"]
    metafunc.parametrize(
        "candidate",
        [
            pytest.param((cases[row["scenario_id"]], row), id=row["id"])
            for row in select_executions(rows, SELECTED_ID)
        ],
    )


def select_executions(rows, selected):
    if selected is None:
        return rows
    matches = [row for row in rows if row["id"] == selected]
    if not matches:
        raise pytest.UsageError(f"Unknown execution ID: {selected}")
    return matches


def report_result(result, record_property):
    record_property("execution_id", result["execution_id"])
    record_property("execution_result", json.dumps(result, sort_keys=True))
    if result["status"] == "blocked":
        pytest.skip(result["reason"])
    assert result["status"] == "passed", result


if not EXPANDED or not (
    SELECTED_TYPED_ID or HOP_PATH or TYPED_SERVICE or NATIVE_ACQUISITION or NATIVE_POLICY or SPIFFE_SUPPORT
):
    def test_peer_execution(candidate, request, peer_setup_cache, record_property):
        case, execution = candidate
        adapters = {}
        if execution["status"] == "qualified":
            if execution.get("native_stage"):
                adapters = request.getfixturevalue("native_workload_adapters")
            elif endpoint_candidates(execution) & {"go-spiffe", "defakto"}:
                adapter = request.getfixturevalue("spiffe_peer_adapter")
                adapters = dict.fromkeys(adapter.families, adapter)
            elif any(endpoint["implementation"] == "cred" and endpoint["profile"] == "wit-http-signature"
                     for pair in execution["pairs"].values() for endpoint in pair.values()):
                adapter = request.getfixturevalue("cred_http_signature_adapter")
                adapters = dict.fromkeys(adapter.families, adapter)
            else:
                adapters = request.getfixturevalue("peer_adapters")
        result, = run_inventory(
            [case], [execution], adapters, setup_cache=peer_setup_cache
        )
        record_property("scenario_id", case["id"])
        report_result(result, record_property)


if EXPANDED and not NATIVE_BASELINE_WORKLOAD and (SELECTED_ID is None or SELECTED_TYPED_ID):
    def test_typed_hop_execution(hop_execution, typed_hop_adapters, record_property):
        result = run_hop_execution(hop_execution, typed_hop_adapters)
        record_property("hop_sequence_id", hop_execution["hop_sequence_id"])
        report_result(result, record_property)
