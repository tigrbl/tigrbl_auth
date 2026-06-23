from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from tigrbl_auth.cli.main import main
from tigrbl_identity_storage_runtime.operator_store import operator_state_root, resource_state_path


def _invoke_json(argv: list[str]) -> tuple[int, dict[str, object]]:
    stream = io.StringIO()
    with redirect_stdout(stream):
        rc = main(argv)
    return rc, json.loads(stream.getvalue())


@pytest.mark.conformance
def test_cli_resource_lifecycle_commands_are_stateful_and_deterministic(tmp_path: Path) -> None:
    repo_root = tmp_path
    scenarios = {
        "tenant": {"create_fields": ["--set", "name=Tenant One"], "toggle": "disable", "expected_status": "disabled"},
        "client": {"create_fields": ["--set", "name=Client One"], "toggle": "disable", "expected_status": "disabled"},
        "identity": {"create_fields": ["--set", "username=user-one"], "toggle": "lock", "expected_status": "locked"},
        "flow": {"create_fields": ["--set", "name=Flow One"], "toggle": "disable", "expected_status": "disabled"},
    }
    for resource, scenario in scenarios.items():
        record_id = f"{resource}-one"
        rc, payload = _invoke_json([resource, "create", "--repo-root", str(repo_root), "--id", record_id, *scenario["create_fields"], "--yes", "--format", "json"])
        assert rc == 0
        assert payload["record"]["id"] == record_id

        rc, payload = _invoke_json([resource, scenario["toggle"], "--repo-root", str(repo_root), "--id", record_id, "--yes", "--format", "json"])
        assert rc == 0
        assert payload["record"]["status"] == scenario["expected_status"]

        rc, payload = _invoke_json([resource, "get", "--repo-root", str(repo_root), "--id", record_id, "--format", "json"])
        assert rc == 0
        assert payload["record"]["id"] == record_id

        rc, payload = _invoke_json([resource, "list", "--repo-root", str(repo_root), "--format", "json"])
        assert rc == 0
        assert any(item["id"] == record_id for item in payload["items"])

    state_root = operator_state_root(repo_root)
    assert (state_root / "operator_plane.sqlite3").exists()
    assert resource_state_path(repo_root, "tenant").exists()
    assert resource_state_path(repo_root, "client").exists()
    assert resource_state_path(repo_root, "identity").exists()
    assert resource_state_path(repo_root, "flow").exists()
    assert repo_root.resolve() not in state_root.resolve().parents
