from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


def test_every_python_package_has_one_exact_uv_source_path() -> None:
    root_data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8-sig"))
    sources = root_data["tool"]["uv"]["sources"]
    manifests: dict[str, str] = {}
    for manifest in PKGS.rglob("pyproject.toml"):
        data = tomllib.loads(manifest.read_text(encoding="utf-8-sig"))
        name = data["project"]["name"]
        manifests[name] = manifest.parent.relative_to(ROOT).as_posix()
    local_sources = {
        name: value["path"].replace("\\", "/")
        for name, value in sources.items()
        if isinstance(value, dict) and "path" in value and value["path"].startswith("pkgs/")
    }
    assert local_sources == manifests


def test_javascript_workspace_members_match_numbered_ui_layers() -> None:
    data = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    declared = set(data["workspaces"])
    discovered = {
        path.parent.relative_to(ROOT).as_posix()
        for layer in (PKGS / "100-uix-core", PKGS / "105-ui")
        for path in layer.glob("*/package.json")
    }
    assert declared == discovered
