"""Keep the Trusted Publishing path scoped to one validated project at a time."""

import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from release_one_standards_package import ensure_source_tag, select_release
import release_one_standards_package as publisher


@pytest.fixture
def release():
    row = dict(name="example", version="1.0.1", path="pkgs/02-contracts/example")
    plan = json.dumps(dict(packages=[row])).encode()
    manifest = dict(
        source_commit="a" * 40,
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


@pytest.mark.parametrize("commit", [None, "", "old-build", "a" * 39])
def test_rejects_artifacts_without_immutable_source(release, commit):
    plan, manifest = release
    if commit is None:
        manifest.pop("source_commit")
    else:
        manifest["source_commit"] = commit
    with pytest.raises(ValueError, match="immutable source"):
        select_release(plan, manifest, "example")


def test_refuses_to_move_an_existing_source_tag(monkeypatch):
    from types import SimpleNamespace
    import release_one_standards_package as publisher

    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout="b" * 40)

    monkeypatch.setattr(publisher.subprocess, "run", run)
    with pytest.raises(ValueError, match="Refusing to replace"):
        ensure_source_tag(dict(name="example", version="1.0.1"), "a" * 40)
    assert len(calls) == 1


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


def test_waits_for_pypi_metadata_propagation(monkeypatch):
    outcomes = iter([False, False, True])
    sleeps = []

    def check(artifact, required):
        assert required
        if not next(outcomes):
            raise publisher.ReleaseIncompleteError("not visible yet")
        return True

    monkeypatch.setattr(publisher, "check", check)
    monkeypatch.setattr(publisher.time, "sleep", sleeps.append)
    publisher.wait_for_pypi_release({}, attempts=3, interval=10)
    assert sleeps == [10, 10]


@pytest.mark.parametrize(
    "error",
    [ValueError("PyPI hash conflict"), publisher.ReleaseIncompleteError("incomplete")],
)
def test_propagation_wait_is_bounded_and_never_retries_hash_conflicts(
    monkeypatch, error
):
    calls, sleeps = [], []

    def check(artifact, required):
        calls.append(artifact)
        raise error

    monkeypatch.setattr(publisher, "check", check)
    monkeypatch.setattr(publisher.time, "sleep", sleeps.append)
    with pytest.raises(type(error)):
        publisher.wait_for_pypi_release({}, attempts=3, interval=10)
    expected = 3 if isinstance(error, publisher.ReleaseIncompleteError) else 1
    assert len(calls) == expected
    assert sleeps == [10] * (expected - 1)


def test_clean_install_refreshes_publishers_negative_index_cache(tmp_path, monkeypatch):
    import verify_standards_installs as installs

    commands = []

    def run(command):
        commands.append(command)
        if "install" in command:
            assert "--refresh" in command
            assert "--no-config" in command
            assert "https://pypi.org/simple/" in command
            raise RuntimeError("stop after checking the real install command")
        return ""

    monkeypatch.setattr(installs, "run", run)
    result = installs.verify(
        dict(name="example", version="1.0.1", import_root="example"),
        tmp_path / "receipts",
        None,
        tmp_path,
    )
    assert result["passed"] is False
    assert "real install command" in result["error"]
    assert any("install" in command for command in commands)
