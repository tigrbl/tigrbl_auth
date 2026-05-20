from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.monorepo_release import discover_packages


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "monorepo_release.py"


def test_monorepo_release_discovers_split_packages() -> None:
    packages = {item.name: item for item in discover_packages()}

    assert len(packages) == 17
    assert packages["tigrbl-auth"].path.as_posix() == "pkgs/tigrbl-auth"
    assert packages["tigrbl-identity-oauth"].import_root == "tigrbl_identity_oauth"


def test_monorepo_release_accepts_package_version_tag() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "resolve-tag", "tigrbl-auth==0.3.5"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert '"name": "tigrbl-auth"' in completed.stdout
    assert '"tag": "tigrbl-auth==0.3.5"' in completed.stdout


def test_monorepo_release_rejects_stale_version_for_split_package() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "resolve-tag", "tigrbl-auth==0.3.4"],
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

    assert payload["count"] == "85"
    assert {
        cell["python_version"]
        for cell in matrix
        if cell["name"] == "tigrbl-identity-core"
    } == {"3.10", "3.11", "3.12", "3.13", "3.14"}
    assert any(
        cell["name"] == "tigrbl-auth"
        and cell["python_version"] == "3.14"
        and cell["cell_id"] == "tigrbl-auth-py314"
        for cell in matrix
    )
    testkit_cells = [cell for cell in matrix if cell["name"] == "tigrbl-identity-testkit"]
    assert len(testkit_cells) == 5
    assert all(cell["cross_cutting"] == "true" for cell in testkit_cells)
    assert all("tests/integration" in cell["package_test_paths"] for cell in testkit_cells)
    assert all("tests/interop" in cell["package_test_paths"] for cell in testkit_cells)


def test_monorepo_release_filters_package_python_test_matrix() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "test-matrix",
            "--package",
            "tigrbl-identity-oauth",
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
            "name": "tigrbl-identity-oauth",
            "version": "0.3.5",
            "path": "pkgs/tigrbl-identity-oauth",
            "import_root": "tigrbl_identity_oauth",
            "tag": "tigrbl-identity-oauth==0.3.5",
            "python_version": "3.12",
            "python_tag": "py312",
            "cell_id": "tigrbl-identity-oauth-py312",
            "workspace_source_globs": "pkgs/*/src",
            "package_test_paths": "tests/packages/tigrbl-identity-oauth\ntests/packages/tigrbl_identity_oauth",
            "pre_test_command": "",
            "cross_cutting": "false",
        }
    ]
