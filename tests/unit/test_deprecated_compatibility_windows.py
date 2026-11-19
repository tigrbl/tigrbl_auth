from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEPRECATED = ROOT / "pkgs" / "deprecated"


def _deprecated_import_roots() -> set[str]:
    return {
        child.name
        for package in DEPRECATED.glob("*/*")
        if package.is_dir()
        for source in (package / "src",)
        if source.is_dir()
        for child in source.iterdir()
        if child.is_dir()
    }


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".", 1)[0])
    return imported


def test_canonical_packages_do_not_depend_on_compatibility_import_roots() -> None:
    deprecated_roots = _deprecated_import_roots()
    violations: list[str] = []

    for source in (ROOT / "pkgs").rglob("*.py"):
        if "deprecated" in source.parts:
            continue
        used = sorted(_imports(source) & deprecated_roots)
        if used:
            violations.append(f"{source.relative_to(ROOT)}: {', '.join(used)}")

    assert violations == []


def test_compatibility_packages_remain_isolated_until_a_release_boundary() -> None:
    packages = [p.parent for p in DEPRECATED.glob("*/*/pyproject.toml")]
    assert packages
    assert {p.name for p in DEPRECATED.iterdir() if p.is_dir()} == {
        "never-lived",
        "undead",
        "dead",
    }
    assert all((package / "src").is_dir() for package in packages)
