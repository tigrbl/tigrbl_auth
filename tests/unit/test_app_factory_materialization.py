from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from tigrbl_auth.cli.install_substrate import build_install_substrate_report

ROOT = Path(__file__).resolve().parents[2]


def test_constraint_files_are_pip_legal_for_clean_room_installs() -> None:
    for relpath in ("constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt", "constraints/test.txt"):
        text = (ROOT / relpath).read_text(encoding="utf-8")
        assert "[asyncio]" not in text
        assert "[email]" not in text
        assert "[standard]" not in text


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


def test_install_substrate_report_tracks_constraint_legalization() -> None:
    payload = build_install_substrate_report(ROOT, execute_import_probes=False)
    assert payload["constraints_consistency"]["passed"] is True
    assert all(not items for items in payload["constraints_consistency"]["illegal_constraint_extras"].values())



def test_introspection_module_uses_runtime_router_when_dependencies_are_installed() -> None:
    pytest.importorskip("sqlalchemy")
    pytest.importorskip("tigrbl")

    import importlib

    module = importlib.reload(importlib.import_module("tigrbl_auth_protocol_oauth.standards.introspection"))

    assert not hasattr(module, "api")
    assert module.introspect_token.__module__ == "tigrbl_identity_storage.tables.token_record._introspection"
    assert module.include_introspection_endpoint.__module__ == "tigrbl_identity_storage.tables.token_record._introspection"
