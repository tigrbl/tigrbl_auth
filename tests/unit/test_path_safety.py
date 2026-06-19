from __future__ import annotations

import json
from pathlib import Path

from tigrbl_auth.path_safety import safe_display_path, sanitize_local_paths
from tigrbl_auth.services._operator_store import operator_store_summary


def test_sanitize_local_paths_redacts_repo_and_host_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    host_path = "C" + ":\\Users\\local\\secret.json"
    payload = {
        "repo_path": str(repo_root / "docs" / "compliance" / "truth_chain.json"),
        "command": f"tigrbl-auth serve --repo-root {repo_root} --out {host_path}",
        "nested": [{"state_root": str(repo_root / ".pytest-tmp" / "operator-state" / "run")}],
    }

    sanitized = sanitize_local_paths(payload, repo_root)
    text = json.dumps(sanitized)

    assert str(repo_root) not in text
    assert "C:" not in text
    assert sanitized["repo_path"] == "<repo>/docs/compliance/truth_chain.json"
    assert "--repo-root <repo>" in sanitized["command"]
    assert sanitized["nested"][0]["state_root"] == "<repo>/.pytest-tmp/operator-state/run"


def test_operator_store_summary_uses_report_safe_paths(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    monkeypatch.setenv("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(tmp_path / "operator-state"))

    summary = operator_store_summary(repo_root)
    text = json.dumps(summary)

    assert str(tmp_path) not in text
    assert ":\\" not in text
    assert summary["state_root"].startswith(("<operator-state>/", "<repo>/"))
    assert summary["audit_log_path"].startswith(("<operator-state>/", "<repo>/"))


def test_safe_display_path_prefers_repo_relative_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    assert (
        safe_display_path(repo_root / "pkgs" / "90-apps" / "admin-uix", repo_root)
        == "pkgs/90-apps/admin-uix"
    )
