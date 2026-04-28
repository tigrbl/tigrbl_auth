from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from tigrbl_auth.cli.install_substrate import build_install_substrate_report

ROOT = Path(__file__).resolve().parents[2]


def test_constraint_files_are_pip_legal_for_clean_room_installs() -> None:
    for relpath in ("constraints/base.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt", "constraints/test.txt"):
        text = (ROOT / relpath).read_text(encoding="utf-8")
        assert "[asyncio]" not in text
        assert "[email]" not in text
        assert "[standard]" not in text


def test_framework_uses_published_tigrbl_api_surface_names() -> None:
    text = (ROOT / "tigrbl_auth" / "framework.py").read_text(encoding="utf-8")
    assert "from tigrbl import APIKey, HTTPBearer, TigrblApi, TigrblApp, engine_ctx, hook_ctx, op_ctx" in text
    assert "class TigrblRouter(TigrblApi)" in text
    assert "from tigrbl.core.crud.params import Header" in text


def test_install_substrate_report_tracks_constraint_legalization() -> None:
    payload = build_install_substrate_report(ROOT, execute_import_probes=False)
    assert payload["constraints_consistency"]["passed"] is True
    assert all(not items for items in payload["constraints_consistency"]["illegal_constraint_extras"].values())



def test_introspection_module_uses_runtime_router_when_dependencies_are_installed() -> None:
    pytest.importorskip("sqlalchemy")
    pytest.importorskip("tigrbl")

    import importlib

    module = importlib.reload(importlib.import_module("tigrbl_auth.standards.oauth2.introspection"))
    routes = list(getattr(module.api, "routes", []))

    assert type(module.api).__module__ == "tigrbl_auth.framework"
    assert routes
    assert any((getattr(route, "path", None) or getattr(route, "path_template", None)) == "/introspect" for route in routes)
    assert all(hasattr(route, "name") for route in routes)
