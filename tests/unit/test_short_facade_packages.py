from __future__ import annotations

import tomllib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("name", ["tba", "tbauth"])
def test_short_facade_is_a_dependency_free_uv_planning_package(name: str) -> None:
    package = ROOT / "pkgs" / "70-facade" / name
    metadata = tomllib.loads((package / "pyproject.toml").read_text(encoding="utf-8"))

    assert metadata["project"]["name"] == name
    assert metadata["project"]["version"] == "0.1.0"
    assert metadata["project"]["dependencies"] == []
    assert "Development Status :: 1 - Planning" in metadata["project"]["classifiers"]
    assert metadata["build-system"]["build-backend"] == "uv_build"
    assert (package / "src" / name / "__init__.py").is_file()
