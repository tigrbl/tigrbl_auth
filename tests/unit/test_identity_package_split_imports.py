from __future__ import annotations

import importlib
import inspect
import sys
from datetime import timedelta
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


DEPRECATED_DIST_NAMES = {
    "tigrbl-authn-credentials",
    "tigrbl-auth-protocol-oidc-backchannel-replay-store",
    "tigrbl-authz-policy-invariant-registry",
    "tigrbl-identity-admin-advanced-authenticator-registry",
    "tigrbl-identity-admin-federation-registry",
    "tigrbl-identity-admin-policy-registry",
    "tigrbl-identity-credentials",
    "tigrbl-identity-policy",
    "tigrbl-identity-oauth",
    "tigrbl-identity-oidc",
    "tigrbl-identity-resource-server",
    "tigrbl-identity-rp",
}

PACKAGE_ROOTS = [
    "tba_contracts_security_trust",
    "tba_bases_security_trust_domain",
    "tba_provider_security_certificate_mtls",
    "tba_provider_security_proof_dpop",
    "tba_provider_security_proof_pkce",
    "tba_provider_security_dpop_cnf_binding_validator",
    "tba_provider_security_mtls_cnf_binding_validator",
    "tigrbl_security_sender_constraint_validator",
    "tba_provider_security_token_introspection_client",
    "tba_provider_security_token_jwks_cache",
    "tba_certification_release",
    "tigrbl_auth_protocol_oidc_backchannel_replay_store",
    "tba_protocol_oauth",
    "tba_protocol_oidc",
    "tba_protocol_oidc_relying_party",
    "tba_credentials",
    "tigrbl_authn_credentials",
    "tigrbl_authz_policy_admin_gate",
    "tba_durability_authorization_policy_authority_derivation_graph",
    "tba_concrete_authority_graph",
    "tba_concrete_authorization_policy_attributes_mapping",
    "tba_concrete_authorization_policy_combiner_default",
    "tba_concrete_authorization_policy_evaluators_default",
    "tba_concrete_authorization_policy_obligations",
    "tba_concrete_authorization_policy_rules",
    "tba_provider_authorization_policy_decision_engine",
    "tigrbl_authz_policy_invariant_registry",
    "tba_runtime_authorization_policy",
    "tba_protocol_authorization_resource_server",
    "tba_provider_authorization_resource_server_verifier",
    "tba_primitives_identity",
    "tba_contracts_identity",
    "tigrbl_identity_credentials_concrete",
    "tigrbl_identity_identities_concrete",
    "tigrbl_identity_admin_advanced_authenticator_registry",
    "tba_provider_identity_admin_auth_anomaly_detector",
    "tigrbl_identity_admin_control_plane",
    "tigrbl_identity_admin_federation_registry",
    "tigrbl_identity_admin_policy_registry",
    "tba_provider_identity_admin_relationship_graph",
    "tba_durability_identity_admin_trust_federation_graph",
    "tba_concrete_trust_federation_graph",
    "tba_concrete_identity_principals",
    "tigrbl_identity_credentials",
    "tba_runtime_identity_authoring",
    "tba_provider_identity_jose",
    "tigrbl_identity_policy",
    "tigrbl_identity_oauth",
    "tigrbl_identity_oidc",
    "tba_runtime_identity_administration",
    "tba_storage_core",
    "tba_server_identity",
    "tba_runtime_identity",
    "tba_operator_identity",
    "tba_cli_identity",
    "tigrbl_identity_resource_server",
    "tigrbl_identity_rp",
    "tba_testkit_identity",
    "tba_provider_security_authorization_provenance_builder",
    "tba_contracts_security_key_rotation_policy",
]

DIST_TO_IMPORT_ROOT = {
    "tba-contracts-security-trust": "tba_contracts_security_trust",
    "tba-bases-security-trust-domain": "tba_bases_security_trust_domain",
    "tba-provider-security-certificate-mtls": "tba_provider_security_certificate_mtls",
    "tba-provider-security-proof-dpop": "tba_provider_security_proof_dpop",
    "tba-provider-security-proof-pkce": "tba_provider_security_proof_pkce",
    "tba-provider-security-dpop-cnf-binding-validator": "tba_provider_security_dpop_cnf_binding_validator",
    "tba-provider-security-mtls-cnf-binding-validator": "tba_provider_security_mtls_cnf_binding_validator",
    "tigrbl-security-sender-constraint-validator": "tigrbl_security_sender_constraint_validator",
    "tba-provider-security-token-introspection-client": "tba_provider_security_token_introspection_client",
    "tba-provider-security-token-jwks-cache": "tba_provider_security_token_jwks_cache",
    "tba-certification-release": "tba_certification_release",
    "tigrbl-auth-protocol-oidc-backchannel-replay-store": "tigrbl_auth_protocol_oidc_backchannel_replay_store",
    "tba-protocol-oauth": "tba_protocol_oauth",
    "tba-protocol-oidc": "tba_protocol_oidc",
    "tba-protocol-oidc-relying-party": "tba_protocol_oidc_relying_party",
    "tba-credentials": "tba_credentials",
    "tigrbl-authn-credentials": "tigrbl_authn_credentials",
    "tigrbl-authz-policy-admin-gate": "tigrbl_authz_policy_admin_gate",
    "tba-durability-authorization-policy-authority-derivation-graph": "tba_durability_authorization_policy_authority_derivation_graph",
    "tba-concrete-authority-graph": "tba_concrete_authority_graph",
    "tba-concrete-authorization-policy-attributes-mapping": "tba_concrete_authorization_policy_attributes_mapping",
    "tba-concrete-authorization-policy-combiner-default": "tba_concrete_authorization_policy_combiner_default",
    "tba-concrete-authorization-policy-evaluators-default": "tba_concrete_authorization_policy_evaluators_default",
    "tba-concrete-authorization-policy-obligations": "tba_concrete_authorization_policy_obligations",
    "tba-concrete-authorization-policy-rules": "tba_concrete_authorization_policy_rules",
    "tba-provider-authorization-policy-decision-engine": "tba_provider_authorization_policy_decision_engine",
    "tigrbl-authz-policy-invariant-registry": "tigrbl_authz_policy_invariant_registry",
    "tba-runtime-authorization-policy": "tba_runtime_authorization_policy",
    "tba-protocol-authorization-resource-server": "tba_protocol_authorization_resource_server",
    "tba-provider-authorization-resource-server-verifier": "tba_provider_authorization_resource_server_verifier",
    "tba-primitives-identity": "tba_primitives_identity",
    "tba-contracts-identity": "tba_contracts_identity",
    "tigrbl-identity-credentials-concrete": "tigrbl_identity_credentials_concrete",
    "tigrbl-identity-identities-concrete": "tigrbl_identity_identities_concrete",
    "tigrbl-identity-admin-advanced-authenticator-registry": "tigrbl_identity_admin_advanced_authenticator_registry",
    "tba-provider-identity-admin-auth-anomaly-detector": "tba_provider_identity_admin_auth_anomaly_detector",
    "tigrbl-identity-admin-control-plane": "tigrbl_identity_admin_control_plane",
    "tigrbl-identity-admin-federation-registry": "tigrbl_identity_admin_federation_registry",
    "tigrbl-identity-admin-policy-registry": "tigrbl_identity_admin_policy_registry",
    "tba-provider-identity-admin-relationship-graph": "tba_provider_identity_admin_relationship_graph",
    "tba-durability-identity-admin-trust-federation-graph": "tba_durability_identity_admin_trust_federation_graph",
    "tba-concrete-trust-federation-graph": "tba_concrete_trust_federation_graph",
    "tba-concrete-identity-principals": "tba_concrete_identity_principals",
    "tigrbl-identity-credentials": "tigrbl_identity_credentials",
    "tba-runtime-identity-authoring": "tba_runtime_identity_authoring",
    "tba-provider-identity-jose": "tba_provider_identity_jose",
    "tigrbl-identity-policy": "tigrbl_identity_policy",
    "tigrbl-identity-oauth": "tigrbl_identity_oauth",
    "tigrbl-identity-oidc": "tigrbl_identity_oidc",
    "tba-runtime-identity-administration": "tba_runtime_identity_administration",
    "tba-storage-core": "tba_storage_core",
    "tba-server-identity": "tba_server_identity",
    "tba-runtime-identity": "tba_runtime_identity",
    "tba-operator-identity": "tba_operator_identity",
    "tba-cli-identity": "tba_cli_identity",
    "tigrbl-identity-resource-server": "tigrbl_identity_resource_server",
    "tigrbl-identity-rp": "tigrbl_identity_rp",
    "tba-testkit-identity": "tba_testkit_identity",
    "tba-auth": "tba_auth",
    "tba-provider-security-authorization-provenance-builder": "tba_provider_security_authorization_provenance_builder",
    "tba-contracts-security-key-rotation-policy": "tba_contracts_security_key_rotation_policy",
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
    assert not (ROOT / "pkgs" / "tba_identity").exists()
    assert not (ROOT / "tba_identity").exists()

    _install_package_src_paths()

    legacy_roots = {path.name for path in (PKGS / "deprecated").glob("*/src/*") if path.is_dir()}
    legacy_roots.update("tba" + name[6:] for name in tuple(legacy_roots) if name.startswith("tigrbl_"))
    for package_root in PACKAGE_ROOTS:
        if package_root in legacy_roots:
            continue
        module = importlib.import_module(package_root)
        assert module.__name__ == package_root


def test_tba_auth_facade_import_root_exists() -> None:
    _install_package_src_paths()

    facade = importlib.import_module("tba_auth")
    assert facade.__name__ == "tba_auth"


def test_split_package_metadata_declares_independent_import_roots() -> None:
    for dist_name, import_root in DIST_TO_IMPORT_ROOT.items():
        package_path = _package_path(dist_name)
        if "deprecated" in package_path.parts:
            continue
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
    for dist_name in ("tba-server-identity",):
        metadata = tomllib.loads(
            (_package_path(dist_name) / "pyproject.toml").read_text(encoding="utf-8")
        )
        dependencies = set(metadata["project"].get("dependencies", []))

        assert any(item.startswith("email-validator") for item in dependencies), (
            dist_name
        )


def test_identity_server_declares_tigrbl_framework_dependency() -> None:
    metadata = tomllib.loads(
        (_package_path("tba-server-identity") / "pyproject.toml").read_text(
            encoding="utf-8"
        )
    )

    dependencies = set(metadata["project"].get("dependencies", []))
    assert "tigrbl==0.4.4.dev1" in dependencies
    assert "tigrbl-core==0.4.4.dev1" in dependencies


def test_oauth_protocol_declares_security_proof_dependencies() -> None:
    metadata = tomllib.loads(
        (_package_path("tba-protocol-oauth") / "pyproject.toml").read_text(
            encoding="utf-8"
        )
    )

    assert not any(
        dependency.startswith("swarmauri_")
        for dependency in metadata["project"].get("dependencies", [])
    )
    assert "tba-provider-security-proof-pkce==0.1.0" in set(
        metadata["project"].get("dependencies", [])
    )


def test_runtime_token_service_exports_async_runtime_helper() -> None:
    _install_package_src_paths()

    module = importlib.import_module("tba_runtime_identity.token_service")
    runtime = importlib.import_module("tba_provider_identity_jose.jwt_runtime")

    assert callable(module._svc_async)
    assert callable(runtime._svc_async)
    assert module._svc_async is runtime._svc_async


def test_runtime_token_service_reuses_token_contract_defaults_and_errors() -> None:
    _install_package_src_paths()

    contracts = importlib.import_module("tba_contracts_identity.tokens")
    module = importlib.import_module("tba_runtime_identity.token_service")
    runtime = importlib.import_module("tba_provider_identity_jose.jwt_runtime")
    runtime_source = (
        _package_path("tba-provider-identity-jose")
        / "src"
        / "tba_provider_identity_jose"
        / "jwt_runtime.py"
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


def test_runtime_token_service_uses_provider_jwt_coder() -> None:
    _install_package_src_paths()

    module = importlib.import_module("tba_runtime_identity.token_service")
    coder_module = importlib.import_module("tba_provider_identity_jose.jwt_coder")

    assert inspect.iscoroutinefunction(module.JWTCoder.async_default)
    assert inspect.iscoroutinefunction(coder_module.JWTCoder.async_default)
    assert module.JWTCoder is coder_module.JWTCoder


def test_credentials_facade_does_not_own_token_or_session_service_modules() -> None:
    _install_package_src_paths()

    credentials_root = (
        _package_path("tba-credentials") / "src" / "tba_credentials"
    )

    assert not (credentials_root / "token_service.py").exists()
    assert not (credentials_root / "session_service.py").exists()
    assert not (credentials_root / "_token_service").exists()

    for module_name in (
        "tba_credentials.token_service",
        "tba_credentials.session_service",
        "tba_credentials._token_service",
    ):
        for loaded_name in list(sys.modules):
            if loaded_name == module_name or loaded_name.startswith(f"{module_name}."):
                sys.modules.pop(loaded_name, None)
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(module_name)


def test_jose_token_paths_require_injected_async_revocation_hooks() -> None:
    coder_source = (
        _package_path("tba-provider-identity-jose")
        / "src"
        / "tba_provider_identity_jose"
        / "jwt_coder.py"
    ).read_text(encoding="utf-8")
    runtime_source = (
        _package_path("tba-provider-identity-jose")
        / "src"
        / "tba_provider_identity_jose"
        / "jwt_runtime.py"
    ).read_text(encoding="utf-8")
    token_persistence_source = (
        _package_path("tba-runtime-identity-storage")
        / "src"
        / "tba_runtime_identity_storage"
        / "token_persistence.py"
    ).read_text(encoding="utf-8")
    server_handler_source = (
        _package_path("tba-server-identity")
        / "src"
        / "tba_server_identity"
        / "security"
        / "handler_records.py"
    ).read_text(encoding="utf-8")

    assert "persist_token: bool = True" in coder_source
    assert "register_token" not in coder_source
    assert "revocation_checker: RevocationChecker | None" in coder_source
    assert "self._revocation_checker(token)" in coder_source
    assert 'runtime["is_revoked_async"]' not in coder_source
    assert "standards.introspection" not in runtime_source
    assert "register_token" not in runtime_source
    assert "standards.revocation" not in runtime_source
    assert "normalize_refresh_audience" in token_persistence_source
    assert "persist_token=False" in server_handler_source


def test_oauth_revocation_exports_protocol_service_only() -> None:
    _install_package_src_paths()

    split_module = importlib.import_module(
        "tba_protocol_oauth.standards.revocation"
    )
    runtime_source = (
        _package_path("tba-provider-identity-jose")
        / "src"
        / "tba_provider_identity_jose"
        / "jwt_runtime.py"
    ).read_text(encoding="utf-8")

    assert hasattr(split_module, "RFC7009RevocationService")
    assert not hasattr(split_module, "revoke_token_async")
    assert not hasattr(split_module, "is_revoked_async")
    assert not hasattr(split_module, "reset_revocations_async")
    assert "standards.revocation" not in runtime_source
    assert "is_revoked_async" not in runtime_source


def test_oauth_introspection_exports_protocol_service_only() -> None:
    _install_package_src_paths()

    split_module = importlib.import_module(
        "tba_protocol_oauth.standards.introspection"
    )
    runtime_source = (
        _package_path("tba-provider-identity-jose")
        / "src"
        / "tba_provider_identity_jose"
        / "jwt_runtime.py"
    ).read_text(encoding="utf-8")

    assert hasattr(split_module, "RFC7662IntrospectionService")
    assert not hasattr(split_module, "register_token_async")
    assert not hasattr(split_module, "introspect_token_async")
    assert not hasattr(split_module, "reset_tokens_async")
    assert "standards.introspection" not in runtime_source
    assert "register_token" not in runtime_source


def test_oidc_backchannel_logout_uses_storage_replay_table() -> None:
    _install_package_src_paths()

    backchannel_logout = importlib.import_module(
        "tba_protocol_oidc.standards.backchannel_logout"
    )
    tables = importlib.import_module("tba_storage_core.tables")
    source = (
        _package_path("tba-protocol-oidc")
        / "src"
        / "tba_protocol_oidc"
        / "standards"
        / "backchannel_logout.py"
    ).read_text(encoding="utf-8")

    assert backchannel_logout.replay_store_snapshot() == {
        "replay_store": "table:BackchannelLogoutReplay"
    }
    assert (
        tables.TABLE_MODEL_BY_NAME["BackchannelLogoutReplay"]
        is tables.BackchannelLogoutReplay
    )
    assert "BackchannelLogoutReplay.handlers.register" not in source
    persistence_source = (
        _package_path("tba-runtime-identity-storage")
        / "src"
        / "tba_runtime_identity_storage"
        / "oidc_persistence.py"
    ).read_text(encoding="utf-8")
    assert "register_backchannel_logout_replay" in persistence_source
    assert "BackchannelLogoutReplay.handlers.register" not in persistence_source
    assert "_REPLAY_STORE" not in source
    assert "tigrbl_auth_protocol_oidc_backchannel_replay_store" not in source


def test_authorize_routes_use_opaque_browser_session_resolver() -> None:
    route_paths = {
        "protocol": _package_path("tba-protocol-oidc")
        / "src"
        / "tba_protocol_oidc"
        / "router.py",
        "protocol_op": _package_path("tba-protocol-oauth")
        / "src"
        / "tba_protocol_oauth"
        / "ops"
        / "authorize.py",
        "storage_authorize_ops": _package_path("tba-storage-core")
        / "src"
        / "tba_storage_core"
        / "tables"
        / "auth_code"
        / "_ops.py",
        "runtime_authorization": _package_path("tba-server-identity")
        / "src"
        / "tba_server_identity"
        / "authorization_runtime.py",
    }

    assert not route_paths["protocol"].exists()
    assert not route_paths["protocol_op"].exists()

    runtime_authorization_source = route_paths["runtime_authorization"].read_text(
        encoding="utf-8"
    )

    assert not route_paths["storage_authorize_ops"].exists()
    assert "authorize_request" in runtime_authorization_source
    assert "resolve_browser_session_record" in runtime_authorization_source
    assert "deployment_from_request(request, settings)" in runtime_authorization_source
    assert "await resolve_browser_session(request)" not in runtime_authorization_source
    assert 'request.cookies.get("sid")' not in runtime_authorization_source
    assert "UUID(sid)" not in runtime_authorization_source
