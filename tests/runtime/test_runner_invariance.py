from __future__ import annotations

from tba_auth.cli.runtime import build_runner_profile_report
from tba_auth.config.deployment import resolve_deployment
from tba_auth.runtime import build_runtime_hash_matrix, registered_runner_names, runner_registry_manifest


def test_runner_profile_hashes_and_registry_are_complete_and_invariant() -> None:
    deployment = resolve_deployment(profile="baseline", runtime_style="standalone")
    matrix = build_runtime_hash_matrix(deployment=deployment, environment="test")
    names = set(registered_runner_names())

    assert names == {"uvicorn", "hypercorn", "tigrcorn"}
    assert set(matrix) == names
    assert len({payload["application_hash"] for payload in matrix.values()}) == 1
    assert len({payload["runtime_hash"] for payload in matrix.values()}) == len(names)

    registry = runner_registry_manifest()
    assert {item["name"] for item in registry} == names
    assert all(item["capabilities"] for item in registry)
    assert all(item["flag_metadata"] for item in registry)

    report = build_runner_profile_report(
        __import__("pathlib").Path(__file__).resolve().parents[2],
        deployment=deployment,
        report_mode="live-probe",
    )
    assert report["summary"]["runner_count"] == 3
    assert report["summary"]["application_hash_invariant"] is True
