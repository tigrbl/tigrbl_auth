from __future__ import annotations

import importlib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(relative_path: str) -> dict:
    return yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))


def test_public_operator_surface_means_public_python_exports_not_state_store() -> None:
    targets = _load_yaml("compliance/targets/operator-targets.yaml")["targets"]
    declared_modules = {
        module
        for target in targets
        for module in target.get("modules", ())
    }

    assert declared_modules
    assert all("_operator_store" not in module for module in declared_modules)
    assert all("operator_store" not in module for module in declared_modules)


def test_facade_does_not_expose_operator_store_as_public_surface() -> None:
    with _package_src_paths_first():
        try:
            importlib.import_module("tigrbl_auth.services._operator_store")
        except ModuleNotFoundError:
            pass
        else:  # pragma: no cover - failure path
            raise AssertionError("operator store must not be a public tigrbl_auth service facade")


def test_operator_store_names_are_not_in_tigrbl_auth_facade_modules() -> None:
    facade_root = ROOT / "pkgs" / "70-facade" / "tigrbl-auth" / "src" / "tigrbl_auth"
    offenders: list[str] = []
    for path in facade_root.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if "_operator_store" in source or "operator_store" in source:
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def _package_src_paths_first():
    import sys
    from contextlib import contextmanager

    @contextmanager
    def _ctx():
        original_path = list(sys.path)
        removed = {
            name: module
            for name, module in sys.modules.items()
            if name == "tigrbl_auth" or name.startswith("tigrbl_auth.")
        }
        for name in list(removed):
            sys.modules.pop(name, None)
        try:
            root_values = {str(ROOT), ""}
            sys.path = [value for value in sys.path if value not in root_values]
            for src in sorted((ROOT / "pkgs").glob("*/*/src")):
                value = str(src)
                if value not in sys.path:
                    sys.path.insert(0, value)
            yield
        finally:
            for name in list(sys.modules):
                if name == "tigrbl_auth" or name.startswith("tigrbl_auth."):
                    sys.modules.pop(name, None)
            sys.modules.update(removed)
            sys.path = original_path

    return _ctx()
