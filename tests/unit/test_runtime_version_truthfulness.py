from __future__ import annotations

from pathlib import Path

from tigrbl_auth.api.app import _runtime_package_version


ROOT = Path(__file__).resolve().parents[2]


def test_runtime_package_version_matches_pyproject_version() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    version_line = next(line for line in pyproject.splitlines() if line.strip().startswith("version"))
    expected = version_line.split("=", 1)[1].strip().strip('"')
    assert _runtime_package_version() == expected
