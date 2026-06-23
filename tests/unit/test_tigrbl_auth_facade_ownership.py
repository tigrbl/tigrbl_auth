from __future__ import annotations

import hashlib
import importlib
import pytest
import sys
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
LARGE_FILE_THRESHOLD = 400


def package_root(name: str) -> Path:
    matches = sorted(PKGS.glob(f"**/{name}/pyproject.toml"))
    assert matches, f"missing package root for {name}"
    return matches[0].parent


def package_src_roots() -> list[Path]:
    return sorted(PKGS.glob("**/src"))


FACADE_PACKAGE = package_root("tigrbl-auth")
FACADE_ROOT = FACADE_PACKAGE / "src" / "tigrbl_auth"


SPLIT_MODULE_PREFIXES = (
    "tigrbl_auth_protocol_",
    "tigrbl_authn_",
    "tigrbl_authz_",
    "tigrbl_identity_",
    "tigrbl_auth_release_certification",
)
TABLE_MODULE_PREFIXES = ("tigrbl_identity_storage",)


FACADE_MODULES = {
    "tigrbl_auth.api.surfaces": "tigrbl_identity_server.surfaces",
    "tigrbl_auth.config.deployment": "tigrbl_identity_runtime.deployment",
    "tigrbl_auth.config.surfaces": "tigrbl_identity_runtime.surfaces",
    "tigrbl_auth.errors": "tigrbl_identity_core.errors",
    "tigrbl_auth.jwtoken": "tigrbl_auth_protocol_oauth.jwtoken",
    "tigrbl_auth.oidc_id_token": "tigrbl_auth_protocol_oidc.id_token",
    "tigrbl_auth.rfc.rfc8693": "tigrbl_auth_protocol_oauth.standards.token_exchange",
    "tigrbl_auth.rfc.rfc7519": "tigrbl_auth_protocol_oauth.standards.json_web_token",
    "tigrbl_auth.rfc.rfc8725": "tigrbl_auth_protocol_oauth.standards.jwt_best_practices",
    "tigrbl_auth.rfc.rfc7517": "tigrbl_identity_jose.standards.rfc7517",
    "tigrbl_auth.rfc.rfc7518": "tigrbl_identity_jose.standards.rfc7518",
    "tigrbl_auth.security.admin_gate": "tigrbl_authz_policy.admin_gate",
    "tigrbl_auth.security.certification": "tigrbl_auth_release_certification.certification",
    "tigrbl_auth.security.runtime_metadata": "tigrbl_authz_resource_server.runtime_metadata",
    "tigrbl_auth.services.advanced_identity_plane": "tigrbl_identity_admin.advanced_identity_plane",
    "tigrbl_auth.services.governance_extension_plane": "tigrbl_authz_policy.governance_extension",
    "tigrbl_auth.services.policy_invariants": "tigrbl_authz_policy_invariant_registry",
    "tigrbl_auth.services.policy_control_plane": "tigrbl_authz_policy.control_plane",
    "tigrbl_auth.services.tenant_discovery": "tigrbl_auth_protocol_oidc.tenant_discovery",
    "tigrbl_auth.standards.jose.rfc7515": "tigrbl_identity_jose.standards.rfc7515",
    "tigrbl_auth.standards.jose.rfc7517": "tigrbl_identity_jose.standards.rfc7517",
    "tigrbl_auth.standards.jose.rfc7518": "tigrbl_identity_jose.standards.rfc7518",
    "tigrbl_auth.standards.oauth2.dpop": "tigrbl_auth_protocol_oauth.standards.dpop",
    "tigrbl_auth.standards.oauth2.rfc9700": "tigrbl_auth_protocol_oauth.standards.oauth_security_bcp",
    "tigrbl_auth.standards.oauth2.resource_verifier_contract": "tigrbl_auth_protocol_oauth.standards.resource_verifier_contract",
    "tigrbl_auth.services.release_posture_plane": "tigrbl_auth_release_certification.release_posture",
    "tigrbl_auth.services.session_service": "tigrbl_identity_storage.session_service",
    "tigrbl_auth.services.token_service": "tigrbl_identity_runtime.token_service",
    "tigrbl_auth.release_signing": "tigrbl_identity_author.release_signing",
    "tigrbl_auth.services.authorization_provenance": "tigrbl_authz_policy.provenance",
    "tigrbl_auth.uix.admin_console": "tigrbl_identity_operator.uix.admin_console",
    "tigrbl_auth.db": "tigrbl_identity_storage.db",
    "tigrbl_auth.tables": "tigrbl_identity_storage.tables",
    "tigrbl_auth.migrations": "tigrbl_identity_storage_runtime.migrations",
    "tigrbl_auth.migrations.helpers": "tigrbl_identity_storage.migrations.helpers",
    "tigrbl_auth.migrations.runtime": "tigrbl_identity_storage_runtime.migrations.runtime",
}

EXECUTABLE_FACADE_MODULES: dict[str, str] = {}

INSTALLED_FACADE_MODULES = {
    key: FACADE_MODULES[key]
    for key in (
        "tigrbl_auth.api.surfaces",
        "tigrbl_auth.config.deployment",
        "tigrbl_auth.config.surfaces",
        "tigrbl_auth.errors",
        "tigrbl_auth.jwtoken",
        "tigrbl_auth.oidc_id_token",
        "tigrbl_auth.security.admin_gate",
        "tigrbl_auth.security.certification",
        "tigrbl_auth.security.runtime_metadata",
        "tigrbl_auth.services.governance_extension_plane",
        "tigrbl_auth.services.policy_invariants",
        "tigrbl_auth.services.policy_control_plane",
        "tigrbl_auth.services.tenant_discovery",
        "tigrbl_auth.release_signing",
        "tigrbl_auth.services.authorization_provenance",
        "tigrbl_auth.standards.jose.rfc7515",
        "tigrbl_auth.standards.jose.rfc7517",
        "tigrbl_auth.standards.jose.rfc7518",
        "tigrbl_auth.standards.oauth2.resource_verifier_contract",
        "tigrbl_auth.db",
        "tigrbl_auth.tables",
        "tigrbl_auth.migrations",
        "tigrbl_auth.migrations.helpers",
        "tigrbl_auth.migrations.runtime",
    )
}


@contextmanager
def source_tree_paths_first():
    original_path = list(sys.path)
    removed_modules = {
        name: module
        for name, module in sys.modules.items()
        if (
            name == "tigrbl_auth"
            or name.startswith("tigrbl_auth.")
            or name.startswith(SPLIT_MODULE_PREFIXES)
        )
        and not name.startswith(TABLE_MODULE_PREFIXES)
    }
    for name in list(removed_modules):
        sys.modules.pop(name, None)
    try:
        root_value = str(ROOT)
        sys.path = [value for value in sys.path if value not in {root_value, ""}]
        for src in package_src_roots():
            value = str(src)
            if value not in sys.path:
                sys.path.insert(0, value)
        yield
    finally:
        for name in list(sys.modules):
            if (
                name == "tigrbl_auth"
                or name.startswith("tigrbl_auth.")
                or (
                    name.startswith(SPLIT_MODULE_PREFIXES)
                    and not name.startswith(TABLE_MODULE_PREFIXES)
                )
            ):
                sys.modules.pop(name, None)
        sys.modules.update(removed_modules)
        sys.path = original_path


@contextmanager
def package_src_paths_only():
    original_path = list(sys.path)
    removed_modules = {
        name: module
        for name, module in sys.modules.items()
        if (
            name == "tigrbl_auth"
            or name.startswith("tigrbl_auth.")
            or name.startswith(SPLIT_MODULE_PREFIXES)
        )
        and not name.startswith(TABLE_MODULE_PREFIXES)
    }
    for name in list(removed_modules):
        sys.modules.pop(name, None)
    try:
        root_values = {str(ROOT), ""}
        sys.path = [value for value in sys.path if value not in root_values]
        for src in package_src_roots():
            value = str(src)
            if value not in sys.path:
                sys.path.insert(0, value)
        yield
    finally:
        for name in list(sys.modules):
            if (
                name == "tigrbl_auth"
                or name.startswith("tigrbl_auth.")
                or (
                    name.startswith(SPLIT_MODULE_PREFIXES)
                    and not name.startswith(TABLE_MODULE_PREFIXES)
                )
            ):
                sys.modules.pop(name, None)
        sys.modules.update(removed_modules)
        sys.path = original_path


def test_legacy_facade_modules_alias_canonical_module_objects() -> None:
    with source_tree_paths_first():
        for legacy_name, canonical_name in FACADE_MODULES.items():
            legacy = importlib.import_module(legacy_name)
            canonical = importlib.import_module(canonical_name)

            assert legacy is canonical


def test_no_legacy_executable_facades_remain() -> None:
    assert EXECUTABLE_FACADE_MODULES == {}


def test_legacy_facade_ops_are_not_supported() -> None:
    assert not (FACADE_ROOT / "ops").exists()


def test_legacy_framework_facade_is_not_supported() -> None:
    with package_src_paths_only():
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("tigrbl_auth.framework")


def test_pqc_touched_facades_do_not_own_runtime_implementation() -> None:
    facade_paths = [
        FACADE_ROOT / "jwtoken.py",
        FACADE_ROOT / "standards" / "jose" / "rfc7515.py",
        FACADE_ROOT / "standards" / "jose" / "rfc7517.py",
        FACADE_ROOT / "standards" / "jose" / "rfc7518.py",
        FACADE_ROOT / "standards" / "oauth2" / "resource_verifier_contract.py",
    ]
    forbidden_tokens = {
        "class JWTCoder",
        "def sign_jws",
        "def verify_jws",
        "def load_pqc",
        "ML_DSA_65_ALG =",
        "sign_pqc_payload",
        "verify_pqc_signature",
        "pqcrypto",
        "ProtectedResourceVerifierContract:",
    }

    for path in facade_paths:
        source = path.read_text(encoding="utf-8")
        assert "alias_module" in source, path.relative_to(ROOT).as_posix()
        for token in forbidden_tokens:
            assert token not in source, f"{path.relative_to(ROOT).as_posix()} owns {token}"


def test_installable_tigrbl_auth_facade_exposes_runtime_legacy_paths() -> None:
    with package_src_paths_only():
        for legacy_name, canonical_name in INSTALLED_FACADE_MODULES.items():
            legacy = importlib.import_module(legacy_name)
            canonical = importlib.import_module(canonical_name)

            assert legacy is canonical


def test_installable_tigrbl_auth_facade_exposes_runtime_package() -> None:
    with package_src_paths_only():
        legacy = importlib.import_module("tigrbl_auth.runtime")
        canonical = importlib.import_module("tigrbl_identity_runtime")

        assert legacy is canonical
        assert legacy.LazyASGIApplication is canonical.LazyASGIApplication


def test_installable_tigrbl_auth_facade_exposes_storage_legacy_submodules() -> None:
    with package_src_paths_only():
        legacy_user = importlib.import_module("tigrbl_auth.tables.user")
        canonical_user = importlib.import_module("tigrbl_identity_storage.tables.user")
        legacy_engine = importlib.import_module("tigrbl_auth.tables.engine")
        canonical_engine = importlib.import_module("tigrbl_identity_storage.tables.engine")
        legacy_revision = importlib.import_module(
            "tigrbl_auth.migrations.versions.0011_delegation_grant_lifecycle_tables"
        )
        canonical_revision = importlib.import_module(
            "tigrbl_identity_storage.migrations.versions.0011_delegation_grant_lifecycle_tables"
        )

        assert legacy_user is canonical_user
        assert legacy_user.User is canonical_user.User
        assert legacy_engine is canonical_engine
        assert legacy_engine.get_db is canonical_engine.get_db
        assert legacy_revision is canonical_revision
        assert legacy_revision.revision == canonical_revision.revision


def test_installable_tigrbl_auth_facade_exposes_rfc_legacy_modules() -> None:
    facade_modules = {
        "tigrbl_auth.rfc.rfc7636_pkce": (
            "tigrbl_auth_protocol_oauth.standards.proof_key_for_code_exchange"
        ),
        "tigrbl_auth.rfc.rfc7662_introspection": (
            "tigrbl_auth_protocol_oauth.standards.introspection"
        ),
        "tigrbl_auth.rfc.rfc8414": "tigrbl_auth_protocol_oauth.standards.authorization_server_metadata_endpoint",
        "tigrbl_auth.rfc.rfc9449_dpop": (
            "tigrbl_auth_protocol_oauth.standards.dpop"
        ),
        "tigrbl_auth.rfc.rfc7515": "tigrbl_identity_jose.standards.rfc7515",
        "tigrbl_auth.rfc.rfc7516": "tigrbl_identity_jose.standards.rfc7516",
        "tigrbl_auth.rfc.rfc7519": "tigrbl_auth_protocol_oauth.standards.json_web_token",
        "tigrbl_auth.rfc.rfc7520": "tigrbl_identity_jose.standards.rfc7520",
        "tigrbl_auth.rfc.rfc8725": "tigrbl_auth_protocol_oauth.standards.jwt_best_practices",
        "tigrbl_auth.rfc.rfc8812": "tigrbl_identity_jose.standards.rfc8812",
    }

    with package_src_paths_only():
        for legacy_name, canonical_name in facade_modules.items():
            legacy = importlib.import_module(legacy_name)
            canonical = importlib.import_module(canonical_name)

            assert legacy is canonical


def test_rfc8785_core_legacy_warns_and_facade_module_is_removed() -> None:
    with package_src_paths_only():
        canonical = importlib.import_module("tigrbl_identity_core.json_canonicalization")

        sys.modules.pop("tigrbl_identity_core.rfc8785", None)
        with pytest.warns(
            DeprecationWarning,
            match="tigrbl_identity_core.json_canonicalization",
        ):
            core_legacy = importlib.import_module("tigrbl_identity_core.rfc8785")

        sys.modules.pop("tigrbl_auth.rfc.rfc8785", None)
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("tigrbl_auth.rfc.rfc8785")

        assert core_legacy.canonicalize is canonical.canonicalize


def test_installable_tigrbl_auth_facade_does_not_advertise_root_only_rfc_symbols() -> None:
    with package_src_paths_only():
        package = importlib.import_module("tigrbl_auth")

        assert "RFC8932_SPEC_URL" not in dir(package)
        assert "enforce_encrypted_dns" not in dir(package)


def test_installable_resource_validation_api_imports_facade_metadata_modules() -> None:
    with package_src_paths_only():
        metadata = importlib.import_module(
            "tigrbl_auth.standards.oauth2.resource_validation_metadata"
        )
        contract = importlib.import_module(
            "tigrbl_auth.standards.oauth2.resource_verifier_contract"
        )
        package = importlib.import_module("tigrbl_auth_api_resource_validation")

        assert metadata.CAPABILITIES_METADATA_PATH == "/metadata/capabilities"
        assert contract.build_protected_resource_verifier_contract().fail_closed is True
        assert package.PRODUCT_SURFACE == "resource-validation-api"


def test_tigrbl_auth_facade_declares_canonical_runtime_dependencies() -> None:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib

    metadata = tomllib.loads(
        (FACADE_PACKAGE / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert set(metadata["project"]["dependencies"]).issuperset(
        {
            "tigrbl-identity-cli==0.4.0.dev2",
            "tigrbl-identity-admin==0.4.0.dev2",
            "tigrbl-identity-author==0.4.0.dev2",
            "tigrbl-authn-credentials==0.4.0.dev2",
            "tigrbl-identity-jose==0.4.0.dev2",
            "tigrbl-auth-protocol-oauth==0.4.0.dev2",
            "tigrbl-identity-operator==0.4.0.dev2",
            "tigrbl-authz-policy-authority-derivation-graph==0.4.0.dev2",
            "tigrbl-authz-policy-concrete==0.4.0.dev2",
            "tigrbl-authz-policy-invariant-registry==0.4.0.dev2",
            "tigrbl-authz-policy==0.4.0.dev2",
            "tigrbl-auth-release-certification==0.4.0.dev2",
            "tigrbl-identity-runtime==0.4.0.dev2",
            "tigrbl-identity-server==0.4.0.dev2",
            "tigrbl-identity-storage==0.4.0.dev2",
            "swarmauri_standard==0.10.0",
            "swarmauri_crypto_paramiko==0.4.0.dev5",
        }
    )


def test_jose_no_longer_owns_protocol_jwt_facades() -> None:
    jose_root = package_root("tigrbl-identity-jose") / "src" / "tigrbl_identity_jose"
    oauth_root = package_root("tigrbl-auth-protocol-oauth") / "src" / "tigrbl_auth_protocol_oauth"
    oidc_root = package_root("tigrbl-auth-protocol-oidc") / "src" / "tigrbl_auth_protocol_oidc"

    assert not (jose_root / "jwtoken.py").exists()
    assert not (jose_root / "jwks_service.py").exists()
    assert not (jose_root / "standards" / "rfc7519.py").exists()
    assert not (jose_root / "standards" / "rfc8725.py").exists()
    assert (oauth_root / "jwtoken.py").exists()
    assert (oauth_root / "standards" / "json_web_token.py").exists()
    assert (oauth_root / "standards" / "jwt_best_practices.py").exists()
    assert (oidc_root / "jwks_service.py").exists()


def test_oauth_standards_use_descriptive_module_names() -> None:
    oauth_standards = (
        package_root("tigrbl-auth-protocol-oauth")
        / "src"
        / "tigrbl_auth_protocol_oauth"
        / "standards"
    )

    descriptive_modules = {
        "bearer_token_usage.py",
        "json_web_token.py",
        "revocation.py",
        "assertion_framework.py",
        "jwt_client_auth.py",
        "dynamic_client_registration.py",
        "client_registration_management.py",
        "authorization_framework.py",
        "token_endpoint.py",
        "proof_key_for_code_exchange.py",
        "introspection.py",
        "native_apps.py",
        "authorization_server_metadata.py",
        "authorization_server_metadata_endpoint.py",
        "legacy_jwt_client_assertions.py",
        "device_authorization.py",
        "token_exchange.py",
        "mutual_tls_client_authentication.py",
        "resource_indicators.py",
        "jwt_best_practices.py",
        "jwt_access_tokens.py",
        "jwt_secured_authorization_requests.py",
        "pushed_authorization_requests.py",
        "issuer_identification.py",
        "rich_authorization_requests.py",
        "oauth_security_bcp.py",
        "protected_resource_metadata.py",
    }
    removed_rfc_modules = {
        "rfc6750.py",
        "rfc7009.py",
        "rfc7519.py",
        "rfc7521.py",
        "rfc7523.py",
        "rfc7591.py",
        "rfc7592.py",
        "rfc6749.py",
        "rfc6749_token.py",
        "rfc7636_pkce.py",
        "rfc9449_dpop.py",
        "rfc7662.py",
        "rfc7662_introspection.py",
        "rfc8252.py",
        "rfc8414.py",
        "rfc8414_metadata.py",
        "rfc8523.py",
        "rfc8628.py",
        "rfc8693.py",
        "rfc8705.py",
        "rfc8707.py",
        "rfc8725.py",
        "rfc9068.py",
        "rfc9101.py",
        "rfc9126.py",
        "rfc9207.py",
        "rfc9396.py",
        "rfc9700.py",
        "rfc9728.py",
    }

    for filename in descriptive_modules:
        assert (oauth_standards / filename).exists()
    for filename in removed_rfc_modules:
        assert not (oauth_standards / filename).exists()


def test_tigrbl_auth_has_no_large_exact_copies_of_split_package_modules() -> None:
    canonical_hashes: dict[str, list[Path]] = {}
    for package_root in package_src_roots():
        if package_root.parent.name == "tigrbl-auth":
            continue
        for path in package_root.rglob("*.py"):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            canonical_hashes.setdefault(digest, []).append(path)

    duplicate_large_files: list[str] = []
    for path in sorted(FACADE_ROOT.rglob("*.py")):
        if len(path.read_text(encoding="utf-8").splitlines()) <= LARGE_FILE_THRESHOLD:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        matches = canonical_hashes.get(digest, [])
        if matches:
            duplicate_large_files.append(
                f"{path.relative_to(ROOT).as_posix()} duplicates "
                f"{matches[0].relative_to(ROOT).as_posix()}"
            )

    assert duplicate_large_files == []
