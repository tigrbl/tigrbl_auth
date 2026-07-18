from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

import pytest

from tigrbl_auth.cli.main import main


def _invoke_json(argv: list[str]) -> tuple[int, dict[str, object]]:
    stream = io.StringIO()
    with redirect_stdout(stream):
        rc = main(argv)
    return rc, json.loads(stream.getvalue())


@pytest.mark.conformance
@pytest.mark.parametrize("runner", ["uvicorn", "hypercorn", "tigrcorn"])
def test_cli_serve_dry_run_emits_runtime_plan_for_each_runner(tmp_path: Path, runner: str) -> None:
    rc, payload = _invoke_json([
        "serve",
        "--repo-root",
        str(Path(__file__).resolve().parents[3]),
        "--server",
        runner,
        "--format",
        "json",
        "--dry-run",
        "--output",
        str(tmp_path / f"{runner}.json"),
    ])
    assert rc == 0
    assert payload["command"] == "serve"
    assert payload["server"] == runner
    assert payload["runtime_plan"]["runner"] == runner
    assert (tmp_path / f"{runner}.json").exists()


@pytest.mark.conformance
def test_cli_serve_check_reports_runner_readiness_in_current_environment() -> None:
    rc, payload = _invoke_json([
        "serve",
        "--repo-root",
        str(Path(__file__).resolve().parents[3]),
        "--server",
        "uvicorn",
        "--format",
        "json",
        "--check",
    ])
    assert payload["command"] == "serve"
    assert payload["launch_mode"] == "check"
    assert payload["selected_runner_profile"]["name"] == "uvicorn"
    assert rc in {0, 1}


@pytest.mark.conformance
def test_cli_serve_live_path_writes_runtime_evidence_when_profile_is_ready(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from tigrbl_identity_cli.cli.handlers import HANDLER_MAP

    serve_globals = HANDLER_MAP["serve"].__globals__
    startup_records: dict[str, object] = {}

    def fake_profile_report(*args, **kwargs):
        return {
            "application_probe": {"passed": True, "app_factory": "tigrbl_auth_backend_app_core.app.build_app", "message": "ok"},
            "summary": {"runner_count": 3, "ready_count": 1, "missing_count": 0, "invalid_count": 0},
            "profiles": [
                {"name": "uvicorn", "status": "ready", "installed": True, "available_module": "uvicorn", "diagnostics": [], "application_hash": "a", "runtime_hash": "b"},
            ],
        }

    def fake_probe_application_factory(*, deployment):
        return SimpleNamespace(passed=True, to_manifest=lambda: {"passed": True, "app_factory": "tigrbl_auth_backend_app_core.app.build_app", "message": "ok"}), object()

    def fake_launch_runtime_profile(repo_root, *, app, plan, adapter, startup_payload, evidence_paths=None):
        paths = evidence_paths or serve_globals["runtime_evidence_paths"](repo_root, plan.runner)
        paths["startup"].write_text(json.dumps({"status": "started", "runner": plan.runner}), encoding="utf-8")
        paths["shutdown"].write_text(json.dumps({"status": "stopped", "runner": plan.runner}), encoding="utf-8")
        startup_records.update({"startup": str(paths["startup"]), "shutdown": str(paths["shutdown"]), "runner": plan.runner})
        return 0

    monkeypatch.setitem(serve_globals, "write_runtime_profile_report", fake_profile_report)
    monkeypatch.setitem(serve_globals, "probe_application_factory", fake_probe_application_factory)
    monkeypatch.setitem(serve_globals, "launch_runtime_profile", fake_launch_runtime_profile)

    rc, payload = _invoke_json([
        "serve",
        "--repo-root",
        str(tmp_path),
        "--server",
        "uvicorn",
        "--format",
        "json",
    ])
    assert rc == 0
    assert payload["runtime_evidence"]["startup"].endswith("-startup.json")
    assert payload["runtime_evidence"]["shutdown"].endswith("-shutdown.json")
    assert Path(startup_records["startup"]).exists()
    assert Path(startup_records["shutdown"]).exists()
