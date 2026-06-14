from __future__ import annotations

import ast
import importlib
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


PREFERRED_TO_COMPAT = {
    "tigrbl_authn_credentials": "tigrbl_identity_credentials",
    "tigrbl_authz_policy": "tigrbl_identity_policy",
    "tigrbl_authz_resource_server": "tigrbl_identity_resource_server",
    "tigrbl_auth_protocol_oauth": "tigrbl_identity_oauth",
    "tigrbl_auth_protocol_oidc": "tigrbl_identity_oidc",
    "tigrbl_auth_protocol_rp": "tigrbl_identity_rp",
}

DIST_TO_IMPORT_ROOT = {
    "tigrbl-authn-credentials": "tigrbl_authn_credentials",
    "tigrbl-authz-policy": "tigrbl_authz_policy",
    "tigrbl-authz-resource-server": "tigrbl_authz_resource_server",
    "tigrbl-auth-protocol-oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl-auth-protocol-oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl-auth-protocol-rp": "tigrbl_auth_protocol_rp",
}


def _install_package_src_paths() -> None:
    for src in PKGS.glob("*/src"):
        value = str(src)
        if value not in sys.path:
            sys.path.insert(0, value)


def _absolute_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imports.add(node.module.split(".")[0])
    return imports


def test_preferred_taxonomy_roots_reexport_compatibility_surfaces() -> None:
    _install_package_src_paths()

    for preferred_root, compat_root in PREFERRED_TO_COMPAT.items():
        preferred = importlib.import_module(preferred_root)
        compat = importlib.import_module(compat_root)

        assert preferred.__name__ == preferred_root
        assert set(preferred.__all__) == set(compat.__all__)
        for name in preferred.__all__:
            assert getattr(preferred, name) is getattr(compat, name), (preferred_root, name)


def test_preferred_taxonomy_package_metadata_is_declared() -> None:
    for dist_name, import_root in DIST_TO_IMPORT_ROOT.items():
        pyproject = PKGS / dist_name / "pyproject.toml"
        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [{"include": import_root, "from": "src"}]


def test_identity_packages_do_not_depend_on_new_authn_authz_behavior_roots() -> None:
    forbidden = {"tigrbl_authn_credentials", "tigrbl_authz_policy", "tigrbl_authz_resource_server"}

    for package in PKGS.glob("tigrbl-identity-*/src/*"):
        if not package.is_dir():
            continue
        for path in package.rglob("*.py"):
            assert _absolute_imports(path).isdisjoint(forbidden), path


def test_authn_authz_protocol_boundaries_have_only_allowed_facade_imports() -> None:
    allowed_imports = {
        "tigrbl_authn_credentials": {"__future__", "tigrbl_identity_credentials"},
        "tigrbl_authz_policy": {"__future__", "tigrbl_identity_policy"},
        "tigrbl_authz_resource_server": {"__future__", "tigrbl_identity_resource_server"},
        "tigrbl_auth_protocol_oauth": {"__future__", "tigrbl_identity_oauth"},
        "tigrbl_auth_protocol_oidc": {"__future__", "tigrbl_identity_oidc"},
        "tigrbl_auth_protocol_rp": {"__future__", "tigrbl_identity_rp"},
    }

    for import_root, allowed in allowed_imports.items():
        package_root = next(PKGS.glob(f"*/src/{import_root}"))
        for path in package_root.rglob("*.py"):
            assert _absolute_imports(path) <= allowed, path
