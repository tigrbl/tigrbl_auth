from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.monorepo_release import _local_dependency_closure, discover_packages


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "monorepo_release.py"


def test_monorepo_release_discovers_split_packages() -> None:
    packages = {item.name: item for item in discover_packages()}

    assert len(packages) == 31
    assert packages["tigrbl-auth"].path.as_posix() == "pkgs/tigrbl-auth"
    assert packages["tigrbl-identity-oauth"].path.as_posix() == "pkgs/deprecated/tigrbl-identity-oauth"
    assert packages["tigrbl-identity-oauth"].import_root == "tigrbl_identity_oauth"
    assert packages["tigrbl-auth-protocol-oauth"].import_root == "tigrbl_auth_protocol_oauth"


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

    assert payload["count"] == "131"
    assert {
        cell["python_version"]
        for cell in matrix
        if cell["name"] == "tigrbl-identity-core"
    } == {"3.10", "3.11", "3.12", "3.13", "3.14"}
    assert {
        cell["python_version"]
        for cell in matrix
        if cell["name"] == "tigrbl-auth"
    } == {"3.10", "3.11", "3.12"}
    assert {
        cell["python_version"]
        for cell in matrix
        if cell["name"] == "tigrbl-identity-jose"
    } == {"3.10", "3.11", "3.12"}
    testkit_cells = [cell for cell in matrix if cell["name"] == "tigrbl-identity-testkit"]
    assert len(testkit_cells) == 3
    assert all(cell["cross_cutting"] == "true" for cell in testkit_cells)
    assert all("tests/integration" in cell["package_test_paths"] for cell in testkit_cells)
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
            "path": "pkgs/tigrbl-auth-protocol-oauth",
            "import_root": "tigrbl_auth_protocol_oauth",
            "tag": "tigrbl-auth-protocol-oauth==0.4.0.dev2",
            "python_version": "3.12",
            "python_tag": "py312",
            "cell_id": "tigrbl-auth-protocol-oauth-py312",
            "workspace_source_globs": "pkgs/*/src\npkgs/deprecated/*/src",
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

    assert dependency_names == {"tigrbl-auth-protocol-oauth"}

    facade_dependency_names = {
        item.name for item in _local_dependency_closure(packages["tigrbl-auth"])
    }
    assert "tigrbl-auth-protocol-oauth" in facade_dependency_names
    assert "tigrbl-identity-storage" in facade_dependency_names

    api_dependency_names = {
        item.name
        for item in _local_dependency_closure(packages["tigrbl-auth-api-developer"])
    }
    assert "tigrbl-auth" in api_dependency_names
    assert "tigrbl-auth-protocol-oauth" in api_dependency_names
