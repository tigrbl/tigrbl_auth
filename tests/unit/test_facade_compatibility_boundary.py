from __future__ import annotations

import ast
import importlib
import sys
import warnings
from contextlib import contextmanager
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


@contextmanager
def isolated_facade_import():
    original_path = list(sys.path)
    removed_modules = {name: module for name, module in sys.modules.items() if name == "tigrbl_auth" or name.startswith("tigrbl_auth.")}
    for name in list(removed_modules):
        sys.modules.pop(name, None)
    try:
        root_values = {str(ROOT), ""}
        sys.path = [value for value in sys.path if value not in root_values]
        for src in (ROOT / "pkgs").glob("*/src"):
            value = str(src)
            if value not in sys.path:
                sys.path.insert(0, value)
        yield
    finally:
        for name in list(sys.modules):
            if name == "tigrbl_auth" or name.startswith("tigrbl_auth."):
                sys.modules.pop(name, None)
        sys.modules.update(removed_modules)
        sys.path = original_path


@pytest.mark.unit
def test_facade_t0_public_surfaces_and_entrypoint_manifest_are_importable() -> None:
    with isolated_facade_import():
        facade = importlib.import_module("tigrbl_auth")
        compat = importlib.import_module("tigrbl_auth.compat")

        assert facade.__file__ and "pkgs" in facade.__file__
        assert "app" in compat.STABLE_ENTRYPOINTS
        assert compat.STABLE_ENTRYPOINTS["app"].package == "tigrbl-identity-server"
        assert compat.extras_for("consumer") == ("tigrbl-identity-resource-server", "tigrbl-identity-rp")


@pytest.mark.unit
def test_facade_t1_legacy_imports_are_stable_and_lazy() -> None:
    with isolated_facade_import():
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            app_module = importlib.import_module("tigrbl_auth.app")
            gateway_module = importlib.import_module("tigrbl_auth.gateway")
            plugin_module = importlib.import_module("tigrbl_auth.plugin")
            cli_module = importlib.import_module("tigrbl_auth.cli")

        assert sorted(app_module.__all__) == ["app", "build_app", "build_application_runtime_plan"]
        assert "build_gateway" in gateway_module.__all__
        assert "install" in plugin_module.__all__
        assert "main" in cli_module.__all__
        assert repr(app_module.app).startswith("<LazyCompatEntrypoint")
        assert any("compatibility facade" in str(item.message) for item in captured)


@pytest.mark.unit
def test_facade_t1_extras_map_covers_product_install_groups() -> None:
    with isolated_facade_import():
        compat = importlib.import_module("tigrbl_auth.compat")

        assert "tigrbl-identity-server" in compat.extras_for("server")
        assert "tigrbl-identity-operator" in compat.extras_for("operator")
        assert "tigrbl-identity-oauth" in compat.extras_for("oauth")
        assert "tigrbl-identity-rp" in compat.extras_for("consumer")
        assert set(compat.extras_for("all")).issuperset(set(compat.extras_for("server")))


@pytest.mark.unit
def test_facade_t2_fail_closed_unknowns_and_unavailable_targets() -> None:
    with isolated_facade_import():
        compat = importlib.import_module("tigrbl_auth.compat")
        app_module = importlib.import_module("tigrbl_auth.app")

        with pytest.raises(compat.FacadeImportError, match="unknown tigrbl-auth extra"):
            compat.extras_for("missing")
        with pytest.raises(compat.FacadeImportError, match="unknown tigrbl-auth facade entrypoint"):
            compat.resolve_entrypoint("missing")
        with pytest.raises(compat.FacadeImportError, match="requires tigrbl-identity-server"):
            app_module.build_app()


@pytest.mark.unit
def test_facade_t2_import_boundary_does_not_eagerly_import_split_runtime() -> None:
    files = [
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/__init__.py"),
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/app.py"),
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/gateway.py"),
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/plugin.py"),
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/cli/__init__.py"),
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/compat.py"),
    ]
    forbidden_imports = {
        "tigrbl_identity_server",
        "tigrbl_identity_runtime",
        "tigrbl_identity_operator",
    }

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden_imports)
