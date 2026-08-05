from __future__ import annotations

import importlib.util
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/package_index.py"


def _module():
    spec = importlib.util.spec_from_file_location("package_index", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_repo_wide_index_is_current_and_complete() -> None:
    module = _module()
    expected = module.render(module.discover())
    assert (ROOT / "index.toml").read_text(encoding="utf-8") == expected

    index = tomllib.loads(expected)
    indexed_paths = {item["path"] for item in index["packages"]}
    physical_paths = {
        path.parent.relative_to(ROOT).as_posix()
        for path in (ROOT / "pkgs").glob("*/*/pyproject.toml")
        if "name" in tomllib.loads(path.read_text(encoding="utf-8")).get("project", {})
    }
    assert indexed_paths == physical_paths


def test_orders_are_scoped_to_layers_and_exactly_derived() -> None:
    packages = _module().discover()
    by_name = {package.name: package for package in packages}

    for package in packages:
        dependencies = package.same_layer_dependencies
        expected = 0 if not dependencies else 1 + max(by_name[item].order for item in dependencies)
        assert package.order == expected
        assert all(by_name[item].layer == package.layer for item in dependencies)
        assert all(by_name[item].order < package.order for item in dependencies)


def test_storage_boundaries_have_no_scaffolding_components() -> None:
    by_name = {package.name: package for package in _module().discover()}
    assert "tigrbl-identity-storage-core" not in by_name
    assert "tigrbl-identity-storage-foundation" not in by_name
    assert by_name["tigrbl-identity-storage-tenancy"].order == 0
    assert by_name["tigrbl-identity-storage-principals"].order == 1
