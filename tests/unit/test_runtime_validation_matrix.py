from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from tigrbl_auth.cli import runtime as runtime_module
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.cli.reports import generate_state_reports

ROOT = Path(__file__).resolve().parents[2]


async def _surface_probe_app(scope, receive, send):
    if scope["type"] != "http":
        return
    path = scope.get("path", "")
    body = {}
    if path == "/.well-known/openid-configuration":
        body = {"issuer": "https://issuer.example.com", "jwks_uri": "https://issuer.example.com/.well-known/jwks.json"}
    elif path == "/.well-known/oauth-authorization-server":
        body = {"issuer": "https://issuer.example.com", "jwks_uri": "https://issuer.example.com/.well-known/jwks.json"}
    elif path == "/.well-known/oauth-protected-resource":
        body = {"authorization_servers": ["https://issuer.example.com"], "jwks_uri": "https://issuer.example.com/.well-known/jwks.json"}
    elif path == "/.well-known/jwks.json":
        body = {"keys": [{"kid": "kid-1", "kty": "OKP"}]}
    elif path == "/openapi.json":
        body = {"openapi": "3.1.0", "paths": {"/.well-known/openid-configuration": {}, "/.well-known/jwks.json": {}}}
    else:
        await send({"type": "http.response.start", "status": 404, "headers": []})
        await send({"type": "http.response.body", "body": b"{}"})
        return
    payload = json.dumps(body).encode("utf-8")
    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": payload})


class _SurfaceProbeAppWithState:
    def __init__(self, deployment):
        self.state = SimpleNamespace(tigrbl_auth_deployment=deployment)

    async def __call__(self, scope, receive, send):
        await _surface_probe_app(scope, receive, send)


def test_http_surface_probe_helper_passes_for_expected_endpoints() -> None:
    result = runtime_module.probe_http_surface_endpoints(app=_surface_probe_app)
    assert result["executed"] is True
    assert result["passed"] is True
    assert result["endpoint_count"] == 5
    assert result["failed_count"] == 0



def test_http_surface_probe_helper_skips_inactive_profile_endpoints() -> None:
    deployment = resolve_deployment(profile="baseline")
    result = runtime_module.probe_http_surface_endpoints(
        app=_SurfaceProbeAppWithState(deployment),
        deployment=deployment,
    )
    assert result["executed"] is True
    assert result["passed"] is True
    assert result["endpoint_count"] == 4
    assert all(probe["path"] != "/.well-known/oauth-protected-resource" for probe in result["probes"])


def test_serve_check_helper_parses_json_payload(monkeypatch) -> None:
    class FakeCompletedProcess:
        returncode = 0
        stdout = json.dumps(
            {
                "launch_ready": True,
                "application_probe": {"passed": True, "message": "ok"},
                "selected_runner_profile": {"name": "uvicorn", "status": "ready"},
            }
        )
        stderr = ""

    monkeypatch.setattr(runtime_module.shutil, "which", lambda _name: None)
    monkeypatch.setattr(runtime_module.subprocess, "run", lambda *args, **kwargs: FakeCompletedProcess())
    result = runtime_module.probe_runner_serve_check(ROOT, "uvicorn")
    assert result["passed"] is True
    assert result["launch_ready"] is True
    assert "serve --repo-root" in result["command"]


def test_tox_and_workflows_execute_real_runtime_validation_steps() -> None:
    tox_text = (ROOT / "tox.ini").read_text(encoding="utf-8")
    install_workflow = (ROOT / ".github" / "workflows" / "ci-install-profiles.yml").read_text(encoding="utf-8")
    release_workflow = (ROOT / ".github" / "workflows" / "ci-release-gates.yml").read_text(encoding="utf-8")

    assert "tigrbl-auth serve --check --server uvicorn" in tox_text
    assert "tigrbl-auth serve --check --server hypercorn" in tox_text
    assert "tigrbl-auth serve --check --server tigrcorn" in tox_text
    assert "--probe-surfaces --require-surface-probes" in tox_text
    assert "dist/runtime-smoke" in install_workflow
    assert "dist/runtime-smoke" in release_workflow


def test_state_report_tracks_runtime_execution_probe_fields() -> None:
    payload = generate_state_reports(ROOT)
    summary = payload["current_state"]
    assert "runtime_profile_application_probe_passed" in summary
    assert "runtime_profile_surface_probe_passed" in summary
    assert "runtime_profile_serve_check_passed_count" in summary
    assert "runtime_profile_execution_probe_complete" in summary
