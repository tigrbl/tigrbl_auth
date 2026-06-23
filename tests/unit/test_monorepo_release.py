from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.monorepo_release import (
    _local_dependency_closure,
    _materialize_testkit_interop_artifacts,
    _root_project_package,
    discover_packages,
)


SCRIPT = ROOT / "scripts" / "monorepo_release.py"

REMOVED_HELPER_PACKAGES = {
    "tigrbl-authz-policy-abac-administrator",
    "tigrbl-authz-policy-delegated-administrator",
    "tigrbl-authz-policy-engine",
    "tigrbl-authz-policy-rbac-administrator",
    "tigrbl-authz-policy-service-identity-registry",
    "tigrbl-authz-resource-server-dpop-cnf-binding-validator",
    "tigrbl-authz-resource-server-introspection-client",
    "tigrbl-authz-resource-server-jwks-cache",
    "tigrbl-authz-resource-server-mtls-cnf-binding-validator",
    "tigrbl-authz-resource-server-sender-constraint-validator",
}


def test_monorepo_release_discovers_split_packages() -> None:
    packages = {item.name: item for item in discover_packages()}

    assert len(packages) == 61
    assert "tigrbl-auth-workspace" not in packages
    assert REMOVED_HELPER_PACKAGES.isdisjoint(packages)
    assert packages["tigrbl-identity-contracts"].path.as_posix() == "pkgs/02-contracts/tigrbl-identity-contracts"
    assert packages["tigrbl-security-trust-domain-bases"].path.as_posix() == "pkgs/05-bases/tigrbl-security-trust-domain-bases"
    assert packages["tigrbl-authz-policy-decision-engine"].path.as_posix() == (
        "pkgs/10-concrete/tigrbl-authz-policy-decision-engine"
    )
    assert packages["tigrbl-authz-policy-concrete"].path.as_posix() == "pkgs/10-concrete/tigrbl-authz-policy-concrete"
    assert packages["tigrbl-identity-concrete"].path.as_posix() == "pkgs/10-concrete/tigrbl-identity-concrete"
    assert packages["tigrbl-authz-resource-server-verifier"].path.as_posix() == (
        "pkgs/20-providers/tigrbl-authz-resource-server-verifier"
    )
    assert packages["tigrbl-security-token-jwks-cache"].path.as_posix() == (
        "pkgs/20-providers/tigrbl-security-token-jwks-cache"
    )
    assert packages["tigrbl-authz-policy"].path.as_posix() == "pkgs/40-capabilities/tigrbl-authz-policy"
    assert packages["tigrbl-identity-admin"].path.as_posix() == "pkgs/40-capabilities/tigrbl-identity-admin"
    assert packages["tigrbl-authz-resource-server"].path.as_posix() == "pkgs/50-protocols/tigrbl-authz-resource-server"


def test_monorepo_release_accepts_package_version_tag() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "resolve-tag", "tigrbl-auth==0.4.0.dev2"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert '"name": "tigrbl-auth"' in completed.stdout
    assert '"tag": "tigrbl-auth==0.4.0.dev2"' in completed.stdout


def test_monorepo_release_rejects_stale_version_for_split_package() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "resolve-tag", "tigrbl-auth==0.4.0.dev1"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "does not match tigrbl-auth pyproject version" in completed.stderr


def test_monorepo_release_builds_package_python_test_matrix() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "test-matrix"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(completed.stdout)
    matrix = json.loads(payload["matrix"])

    assert payload["count"] == "249"
    names = {cell["name"] for cell in matrix}
    assert REMOVED_HELPER_PACKAGES.isdisjoint(names)
    assert "tigrbl-security-token-verification" not in names
    assert "tigrbl-authz-resource-server-verifier" in names
    assert "tigrbl-security-token-jwks-cache" in names
    assert {
        cell["python_version"]
        for cell in matrix
        if cell["name"] == "tigrbl-authz-resource-server-verifier"
    } == {"3.10", "3.11", "3.12", "3.13", "3.14"}
    testkit_cells = [cell for cell in matrix if cell["name"] == "tigrbl-identity-testkit"]
    assert len(testkit_cells) == 3
    assert all(cell["cross_cutting"] == "true" for cell in testkit_cells)
    assert all("tests/packages/tigrbl-identity-testkit" in cell["package_test_paths"] for cell in testkit_cells)
    assert all("tests/integration" not in cell["package_test_paths"] for cell in testkit_cells)
    assert all("tests/interop" in cell["package_test_paths"] for cell in testkit_cells)
    assert all(cell["pytest_args"] == "--certification-lane\nall" for cell in testkit_cells)


def test_monorepo_release_filters_package_python_test_matrix() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "test-matrix",
            "--package",
            "tigrbl-auth-protocol-oauth",
            "--python-version",
            "3.12",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(completed.stdout)
    matrix = json.loads(payload["matrix"])

    assert payload["count"] == "1"
    assert matrix == [
        {
            "name": "tigrbl-auth-protocol-oauth",
            "version": "0.4.0.dev2",
            "path": "pkgs/50-protocols/tigrbl-auth-protocol-oauth",
            "import_root": "tigrbl_auth_protocol_oauth",
            "tag": "tigrbl-auth-protocol-oauth==0.4.0.dev2",
            "python_version": "3.12",
            "python_tag": "py312",
            "cell_id": "tigrbl-auth-protocol-oauth-py312",
            "workspace_source_globs": "pkgs/*/*/src\npkgs/deprecated/*/src",
            "package_test_paths": "tests/packages/tigrbl-auth-protocol-oauth\ntests/packages/tigrbl_auth_protocol_oauth",
            "pre_test_command": "",
            "pytest_args": "",
            "cross_cutting": "false",
        }
    ]


def test_monorepo_release_resolves_local_dependency_closure() -> None:
    packages = {item.name: item for item in discover_packages()}

    dependency_names = {
        item.name
        for item in _local_dependency_closure(packages["tigrbl-identity-oauth"])
    }

    assert REMOVED_HELPER_PACKAGES.isdisjoint(dependency_names)
    assert {
        "tigrbl-auth-protocol-oauth",
        "tigrbl-authz-policy",
        "tigrbl-authz-policy-concrete",
        "tigrbl-authz-policy-decision-engine",
        "tigrbl-authz-resource-server",
        "tigrbl-authz-resource-server-verifier",
        "tigrbl-identity-concrete",
        "tigrbl-identity-contracts",
        "tigrbl-identity-core",
        "tigrbl-identity-jose",
        "tigrbl-security-token-jwks-cache",
        "tigrbl-security-trust-contracts",
        "tigrbl-security-trust-domain-bases",
    }.issubset(dependency_names)

    facade_dependency_names = {
        item.name for item in _local_dependency_closure(packages["tigrbl-auth"])
    }
    assert "tigrbl-auth-protocol-oauth" in facade_dependency_names
    assert "tigrbl-identity-author" in facade_dependency_names
    assert "tigrbl-identity-storage" in facade_dependency_names
    assert "tigrbl-authz-policy-invariant-registry" in facade_dependency_names
    assert "tigrbl-security-token-jwks-cache" in facade_dependency_names

    api_dependency_names = {
        item.name
        for item in _local_dependency_closure(packages["tigrbl-auth-api-developer"])
    }
    assert "tigrbl-auth" in api_dependency_names
    assert "tigrbl-auth-protocol-oauth" in api_dependency_names


def test_monorepo_release_resolves_root_first_party_dependency_closure() -> None:
    root_dependency_names = {
        item.name for item in _local_dependency_closure(_root_project_package())
    }

    assert REMOVED_HELPER_PACKAGES.isdisjoint(root_dependency_names)
    assert "tigrbl-authz-resource-server" in root_dependency_names
    assert "tigrbl-authz-resource-server-verifier" in root_dependency_names
    assert "tigrbl-security-token-jwks-cache" in root_dependency_names
    assert "tigrbl-authz-policy-admin-gate" in root_dependency_names
    assert "tigrbl-authz-policy-concrete" in root_dependency_names
    assert "tigrbl-identity-concrete" in root_dependency_names
    assert "tigrbl-identity-author" in root_dependency_names
    assert "tigrbl-auth-protocol-oauth" in root_dependency_names
    assert "tigrbl-identity-server" in root_dependency_names


def test_monorepo_release_materializes_testkit_interop_templates_with_isolated_python(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[list[str], Path | None, bool]] = []

    def fake_run(args: list[str], *, cwd: Path | None = None, check: bool = False) -> None:
        calls.append((args, cwd, check))

    monkeypatch.setattr(subprocess, "run", fake_run)

    _materialize_testkit_interop_artifacts(Path(".venv/bin/python"))

    assert len(calls) == 1
    args, cwd, check = calls[0]
    assert Path(args[0]) == Path(".venv/bin/python")
    assert args[1] == "-c"
    assert "materialize_external_handoff_templates" in args[2]
    assert cwd == ROOT
    assert check is True
