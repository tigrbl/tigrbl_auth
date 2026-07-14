from __future__ import annotations

from pathlib import Path

import pytest

from tigrbl_auth.cli.install_substrate import build_install_substrate_report

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[2]


def test_runtime_package_owns_runner_extras() -> None:
    runtime_pyproject = ROOT / "pkgs" / "60-runtime" / "tigrbl-identity-runtime" / "pyproject.toml"
    manifest = tomllib.loads(
        runtime_pyproject.read_text(encoding="utf-8")
    )
    extras = manifest["project"]["optional-dependencies"]

    assert extras["uvicorn"] == ["uvicorn[standard]==0.41.0"]
    assert extras["hypercorn"] == ["hypercorn==0.18.0"]
    assert extras["tigrcorn"] == ["tigrcorn==0.3.8; python_version >= '3.11'"]
    assert set(extras["servers"]) == {
        "uvicorn[standard]==0.41.0",
        "hypercorn==0.18.0",
        "tigrcorn==0.3.8; python_version >= '3.11'",
    }


def test_framework_facades_are_not_package_surfaces() -> None:
    assert not (
        ROOT / "pkgs" / "70-facade" / "tigrbl-auth" / "src" / "tigrbl_auth" / "framework.py"
    ).exists()
    assert not (
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tigrbl-identity-server"
        / "src"
        / "tigrbl_identity_server"
        / "framework.py"
    ).exists()


def test_install_substrate_report_tracks_extras_consistency() -> None:
    payload = build_install_substrate_report(ROOT, execute_import_probes=False)
    assert payload["extras_consistency"]["passed"] is True
    assert payload["extras_consistency"]["workspace_runner_extras"]["uvicorn"] == [
        "tigrbl-identity-runtime[uvicorn]==0.4.0.dev2"
    ]


def test_introspection_protocol_module_exports_service_not_runtime_router() -> None:
    pytest.importorskip("sqlalchemy")
    pytest.importorskip("tigrbl")

    import importlib

    module = importlib.reload(importlib.import_module("tigrbl_auth_protocol_oauth.standards.introspection"))

    assert not hasattr(module, "api")
    assert not hasattr(module, "introspect_token")
    assert not hasattr(module, "include_introspection_endpoint")
    assert module.RFC7662IntrospectionService.__module__ == (
        "tigrbl_auth_protocol_oauth.standards.introspection"
    )
