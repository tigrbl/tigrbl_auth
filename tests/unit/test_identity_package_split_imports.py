from __future__ import annotations

import importlib
import inspect
import sys
from datetime import timedelta
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


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
    "tigrbl_security_trust_contracts",
    "tigrbl_security_trust_domain_bases",
    "tigrbl_security_certificate_mtls",
    "tigrbl_security_proof_dpop",
    "tigrbl_security_proof_pkce",
    "tigrbl_auth_release_certification",
    "tigrbl_auth_protocol_oauth",
    "tigrbl_auth_protocol_oidc",
    "tigrbl_auth_protocol_rp",
    "tigrbl_authn_credentials",
    "tigrbl_authz_policy_concrete",
    "tigrbl_authz_policy",
    "tigrbl_authz_resource_server",
    "tigrbl_identity_core",
    "tigrbl_identity_contracts",
    "tigrbl_identity_concrete",
    "tigrbl_identity_principals",
    "tigrbl_identity_credentials",
    "tigrbl_identity_author",
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
    "tigrbl-security-trust-contracts": "tigrbl_security_trust_contracts",
    "tigrbl-security-trust-domain-bases": "tigrbl_security_trust_domain_bases",
    "tigrbl-security-certificate-mtls": "tigrbl_security_certificate_mtls",
    "tigrbl-security-proof-dpop": "tigrbl_security_proof_dpop",
    "tigrbl-security-proof-pkce": "tigrbl_security_proof_pkce",
    "tigrbl-auth-release-certification": "tigrbl_auth_release_certification",
    "tigrbl-auth-protocol-oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl-auth-protocol-oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl-auth-protocol-rp": "tigrbl_auth_protocol_rp",
    "tigrbl-authn-credentials": "tigrbl_authn_credentials",
    "tigrbl-authz-policy-concrete": "tigrbl_authz_policy_concrete",
    "tigrbl-authz-policy": "tigrbl_authz_policy",
    "tigrbl-authz-resource-server": "tigrbl_authz_resource_server",
    "tigrbl-identity-core": "tigrbl_identity_core",
    "tigrbl-identity-contracts": "tigrbl_identity_contracts",
    "tigrbl-identity-concrete": "tigrbl_identity_concrete",
    "tigrbl-identity-principals": "tigrbl_identity_principals",
    "tigrbl-identity-credentials": "tigrbl_identity_credentials",
    "tigrbl-identity-author": "tigrbl_identity_author",
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
    matches = sorted(PKGS.glob(f"**/{dist_name}/pyproject.toml"))
    assert matches, dist_name
    return matches[0].parent


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


def test_email_schema_packages_declare_email_validator_dependency() -> None:
    for dist_name in ("tigrbl-identity-server",):
        metadata = tomllib.loads((_package_path(dist_name) / "pyproject.toml").read_text(encoding="utf-8"))
        dependencies = set(metadata["project"].get("dependencies", []))

        assert any(item.startswith("email-validator") for item in dependencies), dist_name


def test_identity_server_declares_tigrbl_framework_dependency() -> None:
    metadata = tomllib.loads(
        (_package_path("tigrbl-identity-server") / "pyproject.toml").read_text(encoding="utf-8")
    )

    dependencies = set(metadata["project"].get("dependencies", []))
    assert "tigrbl==0.4.4.dev1" in dependencies
    assert "tigrbl-core==0.4.4.dev1" in dependencies


def test_oauth_protocol_declares_security_proof_dependencies() -> None:
    metadata = tomllib.loads(
        (_package_path("tigrbl-auth-protocol-oauth") / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert "swarmauri_signing_dpop==0.1.1" in set(metadata["project"].get("dependencies", []))
    assert "tigrbl-security-proof-pkce==0.1.0" in set(metadata["project"].get("dependencies", []))


def test_credentials_token_service_exports_async_runtime_helper() -> None:
    _install_package_src_paths()

    module = importlib.import_module("tigrbl_authn_credentials.token_service")
    runtime = importlib.import_module("tigrbl_authn_credentials._token_service.runtime")

    assert callable(module._svc_async)
    assert callable(runtime._svc_async)


def test_credentials_token_service_reuses_token_contract_defaults_and_errors() -> None:
    _install_package_src_paths()

    contracts = importlib.import_module("tigrbl_identity_contracts.tokens")
    module = importlib.import_module("tigrbl_authn_credentials.token_service")
    runtime = importlib.import_module("tigrbl_authn_credentials._token_service.runtime")
    runtime_source = (
        _package_path("tigrbl-authn-credentials")
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")

    assert contracts.DEFAULT_ACCESS_TOKEN_TTL == timedelta(minutes=60)
    assert contracts.DEFAULT_REFRESH_TOKEN_TTL == timedelta(days=7)
    assert runtime._ACCESS_TTL is contracts.DEFAULT_ACCESS_TOKEN_TTL
    assert runtime._REFRESH_TTL is contracts.DEFAULT_REFRESH_TOKEN_TTL
    assert module.RefreshTokenError is contracts.RefreshTokenError
    assert module.InvalidRefreshTokenError is contracts.InvalidRefreshTokenError
    assert module.RefreshTokenReuseError is contracts.RefreshTokenReuseError
    assert "class RefreshTokenError" not in runtime_source
    assert "DEFAULT_ACCESS_TOKEN_TTL" in runtime_source


def test_credentials_jwt_coder_exports_async_default_factory() -> None:
    _install_package_src_paths()

    module = importlib.import_module("tigrbl_authn_credentials.token_service")
    coder_module = importlib.import_module("tigrbl_authn_credentials._token_service.coder")

    assert inspect.iscoroutinefunction(module.JWTCoder.async_default)
    assert inspect.iscoroutinefunction(coder_module.JWTCoder.async_default)


def test_credentials_async_token_paths_use_async_persistence_hooks() -> None:
    coder_source = (
        _package_path("tigrbl-authn-credentials")
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "coder.py"
    ).read_text(encoding="utf-8")
    runtime_source = (
        _package_path("tigrbl-authn-credentials")
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")
    credentials_persistence_source = (
        _package_path("tigrbl-authn-credentials")
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "persistence.py"
    ).read_text(encoding="utf-8")
    server_handler_source = (
        _package_path("tigrbl-identity-server")
        / "src"
        / "tigrbl_identity_server"
        / "security"
        / "handler_records.py"
    ).read_text(encoding="utf-8")

    assert "persist_token: bool = True" in coder_source
    assert "register_token" not in coder_source
    assert 'runtime["is_revoked_async"]' in coder_source
    assert 'runtime["is_revoked"](' not in coder_source
    assert "standards.introspection" not in runtime_source
    assert "register_token" not in runtime_source
    assert '"is_revoked_async": is_revoked_async' in runtime_source
    assert "persist_token=False" in credentials_persistence_source
    assert "persist_token=False" in server_handler_source


def test_oauth_revocation_exports_async_runtime_hooks() -> None:
    _install_package_src_paths()

    split_module = importlib.import_module("tigrbl_auth_protocol_oauth.standards.revocation")
    runtime_source = (
        _package_path("tigrbl-authn-credentials")
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")

    assert inspect.iscoroutinefunction(split_module.revoke_token_async)
    assert inspect.iscoroutinefunction(split_module.is_revoked_async)
    assert inspect.iscoroutinefunction(split_module.reset_revocations_async)
    assert "from tigrbl_auth_protocol_oauth.standards.revocation import is_revoked, is_revoked_async" in runtime_source


def test_oauth_introspection_exports_async_runtime_hooks() -> None:
    _install_package_src_paths()

    split_module = importlib.import_module("tigrbl_auth_protocol_oauth.standards.introspection")
    runtime_source = (
        _package_path("tigrbl-authn-credentials")
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
        / "runtime.py"
    ).read_text(encoding="utf-8")

    assert inspect.iscoroutinefunction(split_module.register_token_async)
    assert inspect.iscoroutinefunction(split_module.introspect_token_async)
    assert inspect.iscoroutinefunction(split_module.reset_tokens_async)
    assert "standards.introspection" not in runtime_source
    assert "register_token" not in runtime_source


def test_authorize_routes_use_opaque_browser_session_resolver() -> None:
    route_paths = {
        "protocol": _package_path("tigrbl-auth-protocol-oidc")
        / "src"
        / "tigrbl_auth_protocol_oidc"
        / "router.py",
        "protocol_op": _package_path("tigrbl-auth-protocol-oauth")
        / "src"
        / "tigrbl_auth_protocol_oauth"
        / "ops"
        / "authorize.py",
        "storage_authorize_route": _package_path("tigrbl-identity-storage")
        / "src"
        / "tigrbl_identity_storage"
        / "tables"
        / "auth_code"
        / "_op.py",
        "storage_authorize_logic": _package_path("tigrbl-identity-storage")
        / "src"
        / "tigrbl_identity_storage"
        / "tables"
        / "auth_code"
        / "_op.py",
    }

    assert not route_paths["protocol"].exists()
    assert not route_paths["protocol_op"].exists()

    storage_route_source = route_paths["storage_authorize_route"].read_text(encoding="utf-8")
    storage_logic_source = route_paths["storage_authorize_logic"].read_text(encoding="utf-8")

    assert "authorize_request" in storage_route_source
    assert "resolve_browser_session_record" in storage_logic_source
    assert "deployment_from_request(request, settings)" in storage_logic_source
    assert "await resolve_browser_session(request)" not in storage_logic_source
    assert 'request.cookies.get("sid")' not in storage_logic_source
    assert "UUID(sid)" not in storage_logic_source
