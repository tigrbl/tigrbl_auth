"""Static checks for maintained README source; these do not certify runtime behavior."""
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import pytest

@pytest.mark.unit
def test_readme_example_sources():
    root = Path(__file__).resolve().parents[2]
    settings = tomllib.loads((root / "pyproject.toml").read_text("utf-8"))["tool"]["readme_standards"]
    for example in settings["examples"].values():
        source = root / example["source"]
        assert source.is_file() and source.read_text("utf-8").strip()
        if example.get("language", "python") == "python":
            compile(source.read_text("utf-8"), str(source), "exec")
