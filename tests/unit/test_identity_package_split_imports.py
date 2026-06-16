from __future__ import annotations

import importlib
import inspect
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


DEPRECATED_DIST_NAMES = {
    "tigrbl-identity-credentials",
    "tigrbl-identity-policy",
    "tigrbl-identity-oauth",
    "tigrbl-identity-oidc",
    "tigrbl-identity-resource-server",
    "tigrbl-identity-rp",
}

PACKAGE_ROOTS = [
    "tigrbl_auth_protocol_oauth",
    "tigrbl_auth_protocol_oidc",
    "tigrbl_auth_protocol_rp",
    "tigrbl_authn_credentials",
    "tigrbl_authz_policy",
    "tigrbl_authz_resource_server",
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
    "tigrbl-auth-protocol-oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl-auth-protocol-oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl-auth-protocol-rp": "tigrbl_auth_protocol_rp",
    "tigrbl-authn-credentials": "tigrbl_authn_credentials",
    "tigrbl-authz-policy": "tigrbl_authz_policy",
    "tigrbl-authz-resource-server": "tigrbl_authz_resource_server",
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
    for src in PKGS.rglob("src"):
        value = str(src)
        if value not in sys.path:
            sys.path.append(value)


def _package_path(dist_name: str) -> Path:
    if dist_name in DEPRECATED_DIST_NAMES:
        return PKGS / "deprecated" / dist_name
    return PKGS / dist_name


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
        package_path = _package_path(dist_name)
        pyproject = package_path / "pyproject.toml"
        package_root = package_path / "src" / import_root

        assert pyproject.exists(), dist_name
        assert package_root.is_dir(), import_root

        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [
            {"include": import_root, "from": "src"}
        ]


def test_email_contract_packages_declare_email_validator_dependency() -> None:
    for dist_name in ("tigrbl-identity-contracts", "tigrbl-identity-server"):
        metadata = tomllib.loads((_package_path(dist_name) / "pyproject.toml").read_text(encoding="utf-8"))
        dependencies = set(metadata["project"].get("dependencies", []))

        assert any(item.startswith("email-validator") for item in dependencies), dist_name


def test_credentials_token_service_exports_async_runtime_helper() -> None:
    _install_package_src_paths()

    module = importlib.import_module("tigrbl_authn_credentials.token_service")
    runtime = importlib.import_module("tigrbl_authn_credentials._token_service.runtime")

    assert callable(module._svc_async)
    assert callable(runtime._svc_async)


def test_credentials_jwt_coder_exports_async_default_factory() -> None:
    _install_package_src_paths()

    module = importlib.import_module("tigrbl_authn_credentials.token_service")
    coder_module = importlib.import_module("tigrbl_authn_credentials._token_service.coder")

    assert inspect.iscoroutinefunction(module.JWTCoder.async_default)
    assert inspect.iscoroutinefunction(coder_module.JWTCoder.async_default)


def test_credentials_async_token_paths_use_async_persistence_hooks() -> None:
    coder_source = (
        PKGS
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "coder.py"
    ).read_text(encoding="utf-8")
    runtime_source = (
        PKGS
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")
    credentials_persistence_source = (
        PKGS
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "persistence.py"
    ).read_text(encoding="utf-8")
    server_handler_source = (
        PKGS
        / "tigrbl-identity-server"
        / "src"
        / "tigrbl_identity_server"
        / "security"
        / "handler_records.py"
    ).read_text(encoding="utf-8")

    assert "persist_token: bool = True" in coder_source
    assert 'runtime["register_token_async"]' in coder_source
    assert 'runtime["register_token"](' not in coder_source
    assert 'runtime["is_revoked_async"]' in coder_source
    assert 'runtime["is_revoked"](' not in coder_source
    assert '"register_token_async": register_token_async' in runtime_source
    assert '"is_revoked_async": is_revoked_async' in runtime_source
    assert "persist_token=False" in credentials_persistence_source
    assert "persist_token=False" in server_handler_source


def test_oauth_revocation_exports_async_runtime_hooks() -> None:
    _install_package_src_paths()

    split_module = importlib.import_module("tigrbl_auth_protocol_oauth.standards.revocation")
    facade_module = importlib.import_module("tigrbl_auth.standards.oauth2.revocation")
    runtime_source = (
        PKGS
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")

    assert inspect.iscoroutinefunction(split_module.revoke_token_async)
    assert inspect.iscoroutinefunction(split_module.is_revoked_async)
    assert inspect.iscoroutinefunction(split_module.reset_revocations_async)
    assert inspect.iscoroutinefunction(facade_module.revoke_token_async)
    assert inspect.iscoroutinefunction(facade_module.is_revoked_async)
    assert inspect.iscoroutinefunction(facade_module.reset_revocations_async)
    assert "from tigrbl_auth_protocol_oauth.standards.revocation import is_revoked, is_revoked_async" in runtime_source


def test_oauth_introspection_exports_async_runtime_hooks() -> None:
    _install_package_src_paths()

    split_module = importlib.import_module("tigrbl_auth_protocol_oauth.standards.introspection")
    runtime_source = (
        PKGS
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")

    assert inspect.iscoroutinefunction(split_module.register_token_async)
    assert inspect.iscoroutinefunction(split_module.introspect_token_async)
    assert inspect.iscoroutinefunction(split_module.reset_tokens_async)
    assert "from tigrbl_auth_protocol_oauth.standards.introspection import register_token, register_token_async" in runtime_source


def test_authorize_routes_use_opaque_browser_session_resolver() -> None:
    route_paths = (
        ROOT / "tigrbl_auth" / "routers" / "authz" / "oidc.py",
        PKGS / "tigrbl-auth-protocol-oidc" / "src" / "tigrbl_auth_protocol_oidc" / "router.py",
        PKGS / "tigrbl-identity-server" / "src" / "tigrbl_identity_server" / "routers" / "authz" / "oidc.py",
    )

    for route_path in route_paths:
        source = route_path.read_text(encoding="utf-8")
        assert "resolve_browser_session" in source, route_path
        assert 'request.cookies.get("sid")' not in source, route_path
        assert "UUID(sid)" not in source, route_path
