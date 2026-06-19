from __future__ import annotations

import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tox_pip_install import LocalProject, rewrite_install_args


def test_tox_pip_install_rewrites_first_party_pins_to_local_paths() -> None:
    projects = {
        "tigrbl-auth-protocol-oauth": LocalProject(
            name="tigrbl-auth-protocol-oauth",
            version="0.4.0.dev2",
            path=Path("pkgs/40-protocols/tigrbl-auth-protocol-oauth"),
        )
    }

    assert rewrite_install_args(
        [
            "-c",
            "constraints/base.txt",
            "tigrbl-auth-protocol-oauth==0.4.0.dev2",
            "httpx==0.28.1",
        ],
        projects,
    ) == [
        "-c",
        "constraints/base.txt",
        str(Path("pkgs/40-protocols/tigrbl-auth-protocol-oauth")),
        "httpx==0.28.1",
    ]


def test_tox_pip_install_rejects_stale_first_party_pin() -> None:
    projects = {
        "tigrbl-auth-protocol-oauth": LocalProject(
            name="tigrbl-auth-protocol-oauth",
            version="0.4.0.dev2",
            path=Path("pkgs/40-protocols/tigrbl-auth-protocol-oauth"),
        )
    }

    with pytest.raises(SystemExit, match="does not match local pyproject version"):
        rewrite_install_args(["tigrbl-auth-protocol-oauth==0.4.0.dev1"], projects)


def test_tox_pip_install_leaves_external_and_marker_requirements_unchanged() -> None:
    assert rewrite_install_args(
        [
            "httpx==0.28.1",
            "colorama==0.4.6; platform_system == 'Windows'",
        ],
        {},
    ) == [
        "httpx==0.28.1",
        "colorama==0.4.6; platform_system == 'Windows'",
    ]
