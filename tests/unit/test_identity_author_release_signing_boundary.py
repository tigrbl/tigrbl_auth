from __future__ import annotations

import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTHOR_ROOT = (
    ROOT
    / "pkgs"
    / "60-runtime"
    / "tba-runtime-identity-authoring"
    / "src"
    / "tba_runtime_identity_authoring"
)
JOSE_ROOT = (
    ROOT
    / "pkgs"
    / "20-providers"
    / "tba-provider-identity-jose"
    / "src"
    / "tba_provider_identity_jose"
)


def test_release_signing_lives_in_identity_author() -> None:
    canonical = importlib.import_module("tba_runtime_identity_authoring.release_signing")

    assert (AUTHOR_ROOT / "release_signing").is_dir()
    assert not (JOSE_ROOT / "_release_signing").exists()
    assert callable(canonical.load_signer)
    assert callable(canonical.sha256_bytes)
    assert callable(canonical._canonical_json)


def test_jose_release_signing_bridge_is_removed() -> None:
    assert not (JOSE_ROOT / "release_signing.py").exists()


def test_tba_auth_release_signing_facade_points_to_identity_author() -> None:
    canonical = importlib.import_module("tba_runtime_identity_authoring.release_signing")
    legacy = importlib.import_module("tba_auth.release_signing")

    assert legacy is canonical


def test_release_signing_consumers_do_not_import_jose_owner() -> None:
    source_paths = [
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tba-cli-identity"
        / "src"
        / "tba_cli_identity"
        / "cli"
        / "reports"
        / "_common.py",
        ROOT / "scripts" / "cut_final_release.py",
        ROOT / "scripts" / "sign_release_bundle.py",
    ]

    for path in source_paths:
        source = path.read_text(encoding="utf-8")
        assert "tba_runtime_identity_authoring.release_signing" in source, path
        assert "tba_provider_identity_jose.release_signing" not in source, path
        assert "tba_auth.release_signing" not in source, path
