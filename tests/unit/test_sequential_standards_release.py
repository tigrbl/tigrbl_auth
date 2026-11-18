"""Keep the Trusted Publishing path scoped to one validated project at a time."""

import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from release_one_standards_package import select_release


@pytest.fixture
def release():
    row = dict(name="example", version="1.0.1", path="pkgs/02-contracts/example")
    plan = json.dumps(dict(packages=[row])).encode()
    manifest = dict(
        passed=True,
        failures=[],
        plan_sha256=hashlib.sha256(plan).hexdigest(),
        packages=[dict(row, files=[])],
    )
    return plan, manifest


def test_selects_exactly_the_prepared_project(release):
    row, artifact = select_release(*release, "example")
    assert row["name"] == artifact["name"] == "example"


@pytest.mark.parametrize("name", ["", "all", "unknown"])
def test_cannot_publish_a_batch_or_an_unplanned_project(release, name):
    with pytest.raises(ValueError):
        select_release(*release, name)


def test_rejects_artifacts_from_another_release_plan(release):
    plan, manifest = release
    manifest["plan_sha256"] = "wrong"
    with pytest.raises(ValueError, match="release plan"):
        select_release(plan, manifest, "example")


def test_rejects_mismatched_selected_version(release):
    plan, manifest = release
    manifest["packages"][0]["version"] = "2.0.0"
    with pytest.raises(ValueError, match="version"):
        select_release(plan, manifest, "example")


def test_rejects_a_failed_artifact_batch(release):
    plan, manifest = release
    manifest["passed"] = False
    with pytest.raises(ValueError, match="validation"):
        select_release(plan, manifest, "example")


def test_workflow_uses_oidc_and_the_selected_project_environment():
    workflow = (
        Path(__file__).resolve().parents[2]
        / ".github/workflows/monorepo-package-release.yml"
    ).read_text()
    selected = workflow.split("  publish-one-standards-package:", 1)[1]
    assert "id-token: write" in selected
    assert "name: pypi-${{ inputs.package }}" in selected
    assert "pypi-trusted-publish@" in selected
    assert "packages-dir: prepared-dist" in selected
    assert "PYPI_API_TOKEN" not in workflow
    assert "--phase verify" in selected
    assert "group: monorepo-package-release-trusted-sequential" in workflow
