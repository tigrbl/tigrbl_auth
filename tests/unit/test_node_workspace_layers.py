from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_node_workspaces_use_canonical_uix_layers() -> None:
    manifest = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    workspaces = tuple(manifest["workspaces"])

    assert workspaces
    assert all(
        workspace.startswith(("pkgs/100-uix-core/", "pkgs/105-ui/"))
        for workspace in workspaces
    )
    assert all((ROOT / workspace / "package.json").is_file() for workspace in workspaces)


def test_node_workspaces_do_not_reference_retired_uix_layers() -> None:
    checked = (
        ROOT / "package.json",
        ROOT / "package-lock.json",
        ROOT / ".github" / "workflows" / "package-node-matrix.yml",
        ROOT / ".github" / "workflows" / "monorepo-npm-package-release.yml",
    )

    for path in checked:
        text = path.read_text(encoding="utf-8")
        assert "pkgs/90-uix-core" not in text
        assert "pkgs/95-ui" not in text
