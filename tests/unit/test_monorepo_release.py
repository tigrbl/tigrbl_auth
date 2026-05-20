from __future__ import annotations

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
