from __future__ import annotations

import importlib
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


PACKAGE_ROOTS = [
    "tigrbl_identity_core",
    "tigrbl_identity_contracts",
    "tigrbl_identity_principals",
    "tigrbl_identity_credentials",
    "tigrbl_identity_jose",
    "tigrbl_identity_policy",
    "tigrbl_identity_oauth",
    "tigrbl_identity_oidc",
    "tigrbl_identity_admin",
    "tigrbl_identity_storage",
    "tigrbl_identity_server",
    "tigrbl_identity_runtime",
    "tigrbl_identity_operator",
    "tigrbl_identity_cli",
    "tigrbl_identity_resource_server",
    "tigrbl_identity_rp",
    "tigrbl_identity_testkit",
]

DIST_TO_IMPORT_ROOT = {
    "tigrbl-identity-core": "tigrbl_identity_core",
    "tigrbl-identity-contracts": "tigrbl_identity_contracts",
    "tigrbl-identity-principals": "tigrbl_identity_principals",
    "tigrbl-identity-credentials": "tigrbl_identity_credentials",
    "tigrbl-identity-jose": "tigrbl_identity_jose",
    "tigrbl-identity-policy": "tigrbl_identity_policy",
    "tigrbl-identity-oauth": "tigrbl_identity_oauth",
    "tigrbl-identity-oidc": "tigrbl_identity_oidc",
    "tigrbl-identity-admin": "tigrbl_identity_admin",
    "tigrbl-identity-storage": "tigrbl_identity_storage",
    "tigrbl-identity-server": "tigrbl_identity_server",
    "tigrbl-identity-runtime": "tigrbl_identity_runtime",
    "tigrbl-identity-operator": "tigrbl_identity_operator",
    "tigrbl-identity-cli": "tigrbl_identity_cli",
    "tigrbl-identity-resource-server": "tigrbl_identity_resource_server",
    "tigrbl-identity-rp": "tigrbl_identity_rp",
    "tigrbl-identity-testkit": "tigrbl_identity_testkit",
    "tigrbl-auth": "tigrbl_auth",
}


def _install_package_src_paths() -> None:
    for src in PKGS.glob("*/src"):
        value = str(src)
        if value not in sys.path:
            sys.path.append(value)


def test_identity_split_uses_independent_import_roots() -> None:
    assert not (ROOT / "pkgs" / "tigrbl_identity").exists()
    assert not (ROOT / "tigrbl_identity").exists()

    _install_package_src_paths()

    for package_root in PACKAGE_ROOTS:
        module = importlib.import_module(package_root)
        assert module.__name__ == package_root


def test_tigrbl_auth_facade_import_root_exists() -> None:
    _install_package_src_paths()

    facade = importlib.import_module("tigrbl_auth")
    assert facade.__name__ == "tigrbl_auth"


def test_split_package_metadata_declares_independent_import_roots() -> None:
    for dist_name, import_root in DIST_TO_IMPORT_ROOT.items():
        pyproject = PKGS / dist_name / "pyproject.toml"
        package_root = PKGS / dist_name / "src" / import_root

        assert pyproject.exists(), dist_name
        assert package_root.is_dir(), import_root

        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [
            {"include": import_root, "from": "src"}
        ]
