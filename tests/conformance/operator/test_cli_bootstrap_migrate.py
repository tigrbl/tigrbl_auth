from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from tba_auth.cli.main import main


def _invoke_json(argv: list[str]) -> tuple[int, dict[str, object] | None]:
    stream = io.StringIO()
    with redirect_stdout(stream):
        rc = main(argv)
    raw = stream.getvalue().strip()
    payload = json.loads(raw) if raw.startswith("{") else None
    return rc, payload


@pytest.mark.conformance
def test_cli_bootstrap_and_migrate_lifecycle_commands_round_trip(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[3]

    rc, payload = _invoke_json(["bootstrap", "status", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and payload["command"] == "bootstrap.status"

    rc, payload = _invoke_json(["bootstrap", "manifest", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and payload["manifest"].endswith("deployment.json")

    rc, payload = _invoke_json(["bootstrap", "apply", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and payload["record"]["manifest"].endswith("deployment.json")

    rc, payload = _invoke_json(["bootstrap", "verify", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and payload["passed"] is True

    rc, payload = _invoke_json(["migrate", "status", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and payload["revision_count"] >= 0

    rc, payload = _invoke_json(["migrate", "plan", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and payload["command"] == "migrate.plan"

    rc, payload = _invoke_json(["migrate", "apply", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
    assert payload and "plan_summary" in payload["record"]

    stream = io.StringIO()
    with redirect_stdout(stream):
        rc = main(["migrate", "verify", "--repo-root", str(repo_root), "--format", "json"])
    assert rc == 0
