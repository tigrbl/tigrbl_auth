from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
AUTHOR_ROOT = (
    ROOT
    / "pkgs"
    / "60-runtime"
    / "tigrbl-identity-author"
    / "src"
    / "tigrbl_identity_author"
)
JOSE_ROOT = (
    ROOT
    / "pkgs"
    / "10-domain"
    / "tigrbl-identity-jose"
    / "src"
    / "tigrbl_identity_jose"
)


def test_release_signing_lives_in_identity_author() -> None:
    canonical = importlib.import_module("tigrbl_identity_author.release_signing")

    assert (AUTHOR_ROOT / "release_signing").is_dir()
    assert not (JOSE_ROOT / "_release_signing").exists()
    assert callable(canonical.load_signer)
    assert callable(canonical.sha256_bytes)
    assert callable(canonical._canonical_json)


def test_jose_release_signing_is_deprecated_bridge() -> None:
    canonical = importlib.import_module("tigrbl_identity_author.release_signing")
    sys.modules.pop("tigrbl_identity_jose.release_signing", None)

    with pytest.warns(DeprecationWarning, match="tigrbl_identity_author.release_signing"):
        legacy = importlib.import_module("tigrbl_identity_jose.release_signing")

    assert legacy.load_signer is canonical.load_signer
    assert legacy._canonical_json is canonical._canonical_json


def test_tigrbl_auth_release_signing_facade_points_to_identity_author() -> None:
    canonical = importlib.import_module("tigrbl_identity_author.release_signing")
    legacy = importlib.import_module("tigrbl_auth.release_signing")

    assert legacy is canonical


def test_release_signing_consumers_do_not_import_jose_owner() -> None:
    source_paths = [
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tigrbl-identity-cli"
        / "src"
        / "tigrbl_identity_cli"
        / "cli"
        / "reports"
        / "_common.py",
        ROOT / "scripts" / "cut_final_release.py",
        ROOT / "scripts" / "sign_release_bundle.py",
    ]

    for path in source_paths:
        source = path.read_text(encoding="utf-8")
        assert "tigrbl_identity_author.release_signing" in source, path
        assert "tigrbl_identity_jose.release_signing" not in source, path
        assert "tigrbl_auth.release_signing" not in source, path
