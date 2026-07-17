from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
CORE = PKGS / "100-uix-core"
PRODUCT_UI = PKGS / "105-ui"
IMPORT_RE = re.compile(
    r"(?:from\s+[\"\'](?P<from>[^\"\']+)[\"\']|"
    r"import\s*\(\s*[\"\'](?P<dynamic>[^\"\']+)[\"\']\s*\)|"
    r"require\s*\(\s*[\"\'](?P<require>[^\"\']+)[\"\']\s*\))"
)
SOURCE_SUFFIXES = {".cjs", ".js", ".jsx", ".mjs", ".ts", ".tsx"}


def _manifest(path: Path) -> dict[str, object]:
    return json.loads((path / "package.json").read_text(encoding="utf-8"))


def _local_dependencies(path: Path) -> set[str]:
    data = _manifest(path)
    result: set[str] = set()
    for table in ("dependencies", "devDependencies", "peerDependencies"):
        values = data.get(table, {})
        if isinstance(values, dict):
            result.update(name for name in values if name.startswith("@tigrbl-auth/"))
    return result


def test_uix_core_does_not_depend_on_product_ui_packages() -> None:
    product_names = {_manifest(path)["name"] for path in PRODUCT_UI.iterdir() if (path / "package.json").is_file()}
    core_packages = [path for path in CORE.iterdir() if (path / "package.json").is_file()]
    assert core_packages
    assert all(_local_dependencies(path).isdisjoint(product_names) for path in core_packages)


def test_product_ui_may_only_consume_local_uix_core_packages() -> None:
    core_names = {_manifest(path)["name"] for path in CORE.iterdir() if (path / "package.json").is_file()}
    product_names = {_manifest(path)["name"] for path in PRODUCT_UI.iterdir() if (path / "package.json").is_file()}
    offenders: dict[str, list[str]] = {}
    for path in PRODUCT_UI.iterdir():
        if not (path / "package.json").is_file():
            continue
        forbidden = sorted(_local_dependencies(path) & product_names - core_names)
        if forbidden:
            offenders[path.name] = forbidden
    assert offenders == {}


def test_uix_core_sources_do_not_reach_into_product_ui_paths() -> None:
    offenders: list[str] = []
    for source in CORE.rglob("*"):
        if source.suffix not in SOURCE_SUFFIXES or "node_modules" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for match in IMPORT_RE.finditer(text):
            specifier = match.group("from") or match.group("dynamic") or match.group("require")
            if "105-ui" in specifier:
                offenders.append(f"{source.relative_to(ROOT)}: {specifier}")
    assert offenders == []
