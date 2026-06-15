from __future__ import annotations

import ast
import importlib
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


COMPAT_TO_PREFERRED = {
    "tigrbl_identity_credentials": "tigrbl_authn_credentials",
    "tigrbl_identity_policy": "tigrbl_authz_policy",
    "tigrbl_identity_resource_server": "tigrbl_authz_resource_server",
    "tigrbl_identity_oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl_identity_oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl_identity_rp": "tigrbl_auth_protocol_rp",
}

DIST_TO_IMPORT_ROOT = {
    "tigrbl-authn-credentials": "tigrbl_authn_credentials",
    "tigrbl-authz-policy": "tigrbl_authz_policy",
    "tigrbl-authz-resource-server": "tigrbl_authz_resource_server",
    "tigrbl-auth-protocol-oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl-auth-protocol-oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl-auth-protocol-rp": "tigrbl_auth_protocol_rp",
}

DEPRECATED_DIST_TO_IMPORT_ROOT = {
    "tigrbl-identity-credentials": "tigrbl_identity_credentials",
    "tigrbl-identity-policy": "tigrbl_identity_policy",
    "tigrbl-identity-resource-server": "tigrbl_identity_resource_server",
    "tigrbl-identity-oauth": "tigrbl_identity_oauth",
    "tigrbl-identity-oidc": "tigrbl_identity_oidc",
    "tigrbl-identity-rp": "tigrbl_identity_rp",
}


def _install_package_src_paths() -> None:
    for src in PKGS.rglob("src"):
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


def test_deprecated_taxonomy_roots_reexport_preferred_surfaces() -> None:
    _install_package_src_paths()

    for compat_root, preferred_root in COMPAT_TO_PREFERRED.items():
        preferred = importlib.import_module(preferred_root)
        compat = importlib.import_module(compat_root)

        assert set(preferred.__all__) == set(compat.__all__)
        for name in preferred.__all__:
            assert getattr(preferred, name) is getattr(compat, name), (preferred_root, name)


def test_preferred_taxonomy_package_metadata_is_declared() -> None:
    for dist_name, import_root in DIST_TO_IMPORT_ROOT.items():
        pyproject = PKGS / dist_name / "pyproject.toml"
        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [{"include": import_root, "from": "src"}]


def test_deprecated_taxonomy_package_metadata_lives_under_deprecated_folder() -> None:
    for dist_name, import_root in DEPRECATED_DIST_TO_IMPORT_ROOT.items():
        package_path = PKGS / "deprecated" / dist_name
        pyproject = package_path / "pyproject.toml"
        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

        assert not (PKGS / dist_name).exists()
        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [{"include": import_root, "from": "src"}]
        assert (package_path / "src" / import_root).is_dir()


def test_deprecated_taxonomy_roots_delegate_to_preferred_roots() -> None:
    for dist_name, import_root in DEPRECATED_DIST_TO_IMPORT_ROOT.items():
        package_root = PKGS / "deprecated" / dist_name / "src" / import_root
        preferred_root = COMPAT_TO_PREFERRED[import_root]
        for path in package_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "_CANONICAL_MODULE" in text, path
            assert preferred_root in text, path
            assert _absolute_imports(path) <= {"__future__", "importlib", "warnings"}, path


def test_authn_authz_protocol_roots_do_not_import_deprecated_roots() -> None:
    deprecated_imports = set(COMPAT_TO_PREFERRED)

    for import_root in DIST_TO_IMPORT_ROOT.values():
        package_root = next(PKGS.glob(f"*/src/{import_root}"))
        for path in package_root.rglob("*.py"):
            imports = _absolute_imports(path)
            assert "tigrbl_auth" not in imports, path
            assert imports.isdisjoint(deprecated_imports), path
