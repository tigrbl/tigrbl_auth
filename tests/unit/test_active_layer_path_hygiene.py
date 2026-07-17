from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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


def test_legacy_layer_directories_are_absent() -> None:
    assert [path for value in LEGACY_LAYER_PATHS if (path := ROOT / value).exists()] == []


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
