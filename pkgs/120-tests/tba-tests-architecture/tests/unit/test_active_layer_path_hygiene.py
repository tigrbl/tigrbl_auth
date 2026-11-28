from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
LEGACY_LAYER_PATHS = (
    "pkgs/80-apis",
    "pkgs/90-uix-core",
    "pkgs/95-ui",
    "pkgs/100-tests",
    "pkgs/101-examples",
    "pkgs/105-examples",
)
ACTIVE_CONFIG = (
    ROOT / "pyproject.toml",
    ROOT / "package.json",
    ROOT / "uv.lock",
)


def test_numbered_layers_sort_in_numeric_order() -> None:
    layers = sorted(
        path.name
        for path in (ROOT / "pkgs").iterdir()
        if path.is_dir() and path.name[0].isdigit()
    )
    assert all(re.fullmatch(r"[0-9]{3}-[a-z][a-z0-9-]*", layer) for layer in layers)
    index = tomllib.loads((ROOT / "index.toml").read_text(encoding="utf-8"))
    indexed = [
        record["layer"]
        for record in index["packages"]
        if record["layer"] != "deprecated"
    ]
    assert indexed == sorted(indexed)
    assert set(indexed) <= set(layers)


def test_repository_collects_test_suites_from_layer_120() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["tool"]["pytest"]["ini_options"]["testpaths"] == ["pkgs/120-tests"]
    assert not list((ROOT / "tests").rglob("test_*.py"))


def test_legacy_layer_directories_are_absent() -> None:
    assert [
        path for value in LEGACY_LAYER_PATHS if (path := ROOT / value).exists()
    ] == []


def test_active_workspace_configuration_has_no_legacy_layer_paths() -> None:
    offenders: dict[str, list[str]] = {}
    paths = list(ACTIVE_CONFIG)
    paths.extend((ROOT / ".github" / "workflows").glob("*.yml"))
    paths.extend((ROOT / ".github" / "workflows").glob("*.yaml"))
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig")
        found = [value for value in LEGACY_LAYER_PATHS if value in text]
        if found:
            offenders[path.relative_to(ROOT).as_posix()] = found
    assert offenders == {}
