from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]


def test_pytest_uses_repo_local_temp_root() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    addopts = pyproject["tool"]["pytest"]["ini_options"]["addopts"]

    assert "--basetemp=.pytest-tmp" in addopts.split()
    assert "/.pytest-tmp" in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
