"""Retired names cannot be published or buried without the right evidence."""

import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from deprecated_lifecycle import STAGES, ensure_release_allowed, verify


def test_repository_deprecation_inventory_is_complete_and_evidenced():
    result = verify()
    assert result["passed"], result["failures"]
    assert set(result["counts"]) == set(STAGES)


@pytest.fixture
def lifecycle(tmp_path):
    base = tmp_path / "pkgs/deprecated"
    for stage in STAGES:
        (base / stage).mkdir(parents=True)
    folder = base / "undead/example"
    folder.mkdir()
    (folder / "pyproject.toml").write_text(
        '[project]\nname="example"\n', encoding="utf-8"
    )
    row = dict(
        name="example",
        stage="undead",
        path="pkgs/deprecated/undead/example",
        pypi=dict(published=True, checked_at="2026-11-19T00:00:00Z"),
    )
    ledger = base / "lifecycle.json"
    ledger.write_text(json.dumps(dict(packages=[row])), encoding="utf-8")
    return tmp_path, ledger, row, folder


def test_final_notice_can_be_selected_for_an_existing_published_package(lifecycle):
    root, _, row, _ = lifecycle
    ensure_release_allowed(row["path"], root)
    assert verify(root)["passed"]


@pytest.mark.parametrize("stage", ["never-lived", "dead"])
def test_never_lived_and_graveyard_names_cannot_be_published(stage):
    with pytest.raises(ValueError, match="must not be published"):
        ensure_release_allowed(f"pkgs/deprecated/{stage}/example")


def test_an_unpublished_name_cannot_be_smuggled_into_undead(lifecycle):
    root, ledger, row, _ = lifecycle
    row["pypi"]["published"] = False
    ledger.write_text(json.dumps(dict(packages=[row])), encoding="utf-8")
    with pytest.raises(ValueError, match="previously published"):
        ensure_release_allowed(row["path"], root)
    assert not verify(root)["passed"]


def test_burial_requires_actual_published_deprecation_and_migration_evidence(lifecycle):
    root, ledger, row, folder = lifecycle
    target = folder.parent.parent / "dead/example"
    folder.rename(target)
    row.update(stage="dead", path="pkgs/deprecated/dead/example")
    ledger.write_text(json.dumps(dict(packages=[row])), encoding="utf-8")
    result = verify(root)
    assert not result["passed"]
    assert any(
        "verified published deprecation and migration" in error
        for error in result["failures"]
    )


def test_prepared_old_artifact_cannot_bypass_archive_policy():
    import hashlib
    from release_one_standards_package import select_release

    row = dict(name="example", version="1.0.0", path="pkgs/deprecated/dead/example")
    plan = json.dumps(dict(packages=[row])).encode()
    manifest = dict(
        passed=True,
        failures=[],
        source_commit="a" * 40,
        plan_sha256=hashlib.sha256(plan).hexdigest(),
        packages=[dict(row, files=[])],
    )
    with pytest.raises(ValueError, match="must not be published"):
        select_release(plan, manifest, "example")


@pytest.mark.parametrize(
    "name", ["tba-provider-security-cose", "tba-provider-jose-swarmauri"]
)
def test_legacy_release_cli_rejects_never_lived_and_dead(name):
    import monorepo_release

    with pytest.raises(SystemExit, match="must not be published"):
        monorepo_release._find_package(name)
