"""Final compatibility releases must provide executable migration destinations."""

import ast
import json
from pathlib import Path
import sys
import tomllib

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from readme_policy import section_errors
from verify_standards_installs import MIGRATION_PROBE

PLAN = json.loads(
    (ROOT / ".ssot/evidence/undead-final-release-plan-20261119.json").read_text()
)["packages"]


@pytest.mark.parametrize("release", PLAN, ids=lambda row: row["name"])
def test_final_release_has_complete_owned_migration_paths(release):
    lifecycle = json.loads((ROOT / "pkgs/deprecated/lifecycle.json").read_text())
    current = next(r for r in lifecycle["packages"] if r["name"] == release["name"])
    folder = ROOT / current["path"]
    project = tomllib.loads((folder / "pyproject.toml").read_text())["project"]
    assert project["version"] == release["version"]
    assert "Development Status :: 7 - Inactive" in project["classifiers"]
    owners = {
        tomllib.loads(p.read_text())["project"]["name"]: p.parent
        for p in ROOT.glob("pkgs/[0-9]*/*/pyproject.toml")
    }
    mappings = {m["legacy"]: m for m in release["migration_modules"]}
    observed = set()
    for source in folder.glob("src/**/*.py"):
        values = {
            n.targets[0].id: ast.literal_eval(n.value)
            for n in ast.parse(source.read_text()).body
            if isinstance(n, ast.Assign)
            and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id in {"_DEPRECATED_MODULE", "_CANONICAL_MODULE"}
        }
        if "_DEPRECATED_MODULE" not in values:
            continue
        mapping = mappings[values["_DEPRECATED_MODULE"]]
        observed.add(mapping["legacy"])
        assert values["_CANONICAL_MODULE"] == mapping["replacement"]
        owner = mapping["distribution"]
        assert any(d.startswith(owner + ">=0.4.0.dev") for d in project["dependencies"])
        target = owners[owner] / "src" / mapping["replacement"].replace(".", "/")
        assert target.with_suffix(".py").is_file() or (target / "__init__.py").is_file()
    assert observed == set(mappings)
    readme = (folder / "README.md").read_text()
    assert not section_errors(readme)
    assert "**Deprecated:**" in readme and "### Migration" in readme
    assert f"https://static.pepy.tech/badge/{release['name']}/month" in readme
    assert "Layer: deprecated / undead" in readme
    assert "docs/assets/tba-brand.png" in readme
    assert (folder / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes()
    assert f"Distribution: {release['name']}" in (folder / "NOTICE").read_text()


@pytest.mark.parametrize("defect", [None, "warning", "export"])
def test_installed_migration_probe_rejects_broken_contracts(
    tmp_path, monkeypatch, defect
):
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    canonical = "migration_probe_canonical"
    legacy = "migration_probe_legacy"
    (tmp_path / f"{canonical}.py").write_text("value = object()\n__all__ = ['value']\n")
    message = (
        "incorrect destination"
        if defect == "warning"
        else f"{legacy} is deprecated; import {canonical} instead."
    )
    value = (
        "value = object()" if defect == "export" else f"from {canonical} import value"
    )
    (tmp_path / f"{legacy}.py").write_text(
        f"import warnings\nwarnings.warn({message!r}, DeprecationWarning)\n{value}\n"
    )
    monkeypatch.setattr(
        sys, "argv", ["probe", json.dumps([dict(legacy=legacy, replacement=canonical)])]
    )
    try:
        if defect:
            with pytest.raises(AssertionError):
                exec(MIGRATION_PROBE, {})
        else:
            exec(MIGRATION_PROBE, {})
    finally:
        sys.modules.pop(legacy, None)
        sys.modules.pop(canonical, None)
