from __future__ import annotations

import ast
import importlib
import importlib.util
from pathlib import Path


def test_storage_does_not_export_provenance_builders() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.provenance") is None


def test_storage_tables_do_not_export_ambient_session_module() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.tables._session") is None

    runtime_session = importlib.import_module("tigrbl_identity_storage_runtime.session")
    assert runtime_session.storage_session.__module__ == "tigrbl_identity_storage_runtime.session"
    assert runtime_session.resolve_storage_provider.__module__ == "tigrbl_identity_storage_runtime.session"


TABLE_MODULE_EXPORTS = {
    "access_review_campaign": ("AccessReviewCampaign",),
    "access_review_decision": ("AccessReviewDecision",),
    "access_review_item": ("AccessReviewItem",),
    "attribute_policy": ("AttributePolicy",),
    "audit_event": ("AuditEvent",),
    "auth_code": ("AuthCode",),
    "auth_session": ("AuthSession",),
    "authentication_challenge": ("AuthenticationChallenge",),
    "authority_derivation_graph": (
        "AuthorityDerivationGraph",
        "AuthorityDerivationGraphNode",
        "AuthorityDerivationGraphEdge",
    ),
    "authorization_server": ("AuthorizationServer",),
    "client": ("Client", "_CLIENT_ID_RE"),
    "client_registration": ("ClientRegistration",),
    "consent": ("Consent",),
    "credential": ("Credential",),
    "credential_audit_event": ("CredentialAuditEvent",),
    "credential_api_key": ("CredentialApiKey",),
    "credential_client_secret": ("CredentialClientSecret",),
    "credential_dpop_key": ("CredentialDpopKey",),
    "credential_mfa_factor": ("CredentialMfaFactor",),
    "credential_mtls_certificate": ("CredentialMtlsCertificate",),
    "credential_password": ("CredentialPassword",),
    "credential_recovery_code": ("CredentialRecoveryCode",),
    "credential_service_key": ("CredentialServiceKey",),
    "credential_webauthn_passkey": ("CredentialWebAuthnPasskey",),
    "device_code": ("DeviceCode",),
    "dpop_nonce": ("DpopNonce",),
    "dpop_replay": ("DpopReplay",),
    "delegated_admin_scope": ("DelegatedAdminScope",),
    "delegation_grant": (
        "DelegationGrant",
        "DelegationGrantRecord",
        "DelegationGrantScope",
        "DelegationGrantProof",
        "DelegationGrantEdge",
        "DelegationGrantTokenLink",
    ),
    "entitlement": ("Entitlement",),
    "entitlement_assignment": ("EntitlementAssignment",),
    "crypto_key": ("CryptoKey",),
    "crypto_key_version": ("CryptoKeyVersion",),
    "key_rotation_event": ("KeyRotationEvent",),
    "key_rotation_policy": ("KeyRotationPolicy",),
    "key_envelope": ("KeyEnvelope",),
    "key_attestation_evidence": ("KeyAttestationEvidence",),
    "logout_state": ("LogoutState",),
    "machine_identity": ("MachineIdentity",),
    "policy": ("Policy",),
    "principal": ("Principal",),
    "principal_key_binding": ("PrincipalKeyBinding",),
    "policy_set": ("PolicySet",),
    "policy_set_member": ("PolicySetMember",),
    "policy_target": ("PolicyTarget",),
    "policy_version": ("PolicyVersion",),
    "pushed_authorization_request": (
        "PushedAuthorizationRequest",
        "DEFAULT_PAR_EXPIRY",
    ),
    "realm": ("Realm",),
    "revoked_token": ("RevokedToken",),
    "residency_zone": ("ResidencyZone",),
    "role": ("Role",),
    "service_identity": ("ServiceIdentity",),
    "subject_alias": ("SubjectAlias",),
    "tenant": ("Tenant",),
    "tenant_membership": ("TenantMembership",),
    "tenant_residency": ("TenantResidency",),
    "token_record": ("TokenRecord",),
    "trust_federation_graph": (
        "TrustFederationGraph",
        "TrustFederationGraphNode",
        "TrustFederationGraphEdge",
    ),
    "user": ("User",),
    "workload_identity": ("WorkloadIdentity",),
}


def test_tigrbl_auth_tables_reexport_canonical_storage_symbols() -> None:
    auth_tables = importlib.import_module("tigrbl_auth.tables")
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")

    for name in storage_tables.__all__:
        assert getattr(auth_tables, name) is getattr(storage_tables, name)

    for module_name, exports in TABLE_MODULE_EXPORTS.items():
        auth_module = importlib.import_module(f"tigrbl_auth.tables.{module_name}")
        storage_module = importlib.import_module(
            f"tigrbl_identity_storage.tables.{module_name}"
        )
        for exported in exports:
            assert getattr(auth_module, exported) is getattr(storage_module, exported)


def test_renamed_identity_credential_tables_do_not_keep_legacy_modules() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")

    for legacy_name in ("ApiKey", "Service", "ServiceKey"):
        assert legacy_name not in storage_tables.__all__
        assert not hasattr(storage_tables, legacy_name)

    for module_name in ("api_key", "service", "service_key"):
        assert importlib.util.find_spec(f"tigrbl_identity_storage.tables.{module_name}") is None
        assert importlib.util.find_spec(f"tigrbl_auth.tables.{module_name}") is None


def test_renamed_crypto_key_tables_do_not_keep_legacy_modules() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")

    for legacy_name in ("Key", "KeyVersion"):
        assert legacy_name not in storage_tables.__all__
        assert not hasattr(storage_tables, legacy_name)

    for module_name in ("key", "key_version"):
        assert importlib.util.find_spec(f"tigrbl_identity_storage.tables.{module_name}") is None
        assert importlib.util.find_spec(f"tigrbl_auth.tables.{module_name}") is None


def test_tigrbl_auth_tables_and_db_facades_reexport_storage_symbols() -> None:
    auth_tables = importlib.import_module("tigrbl_auth.tables")
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    auth_db = importlib.import_module("tigrbl_auth.db")
    runtime_db = importlib.import_module("tigrbl_identity_storage_runtime.engine")

    for name in storage_tables.__all__:
        assert getattr(auth_tables, name) is getattr(storage_tables, name)

    assert auth_db.ENGINE is runtime_db.ENGINE
    assert auth_db.dsn == runtime_db.dsn
    assert auth_db.get_db is runtime_db.get_db

    auth_realm = importlib.import_module("tigrbl_auth.tables.realm")
    storage_realm = importlib.import_module("tigrbl_identity_storage.tables.realm")
    assert auth_realm.Realm is storage_realm.Realm


def test_orm_export_paths_are_not_supported() -> None:
    assert importlib.util.find_spec("tigrbl_auth.orm") is None
    assert importlib.util.find_spec("tigrbl_identity_storage.orm") is None


def test_tigrbl_auth_persistence_facade_reexports_storage_helpers() -> None:
    auth_persistence = importlib.import_module("tigrbl_auth.services.persistence")
    runtime_persistence = importlib.import_module(
        "tigrbl_identity_storage_runtime.persistence"
    )

    for name in runtime_persistence.__all__:
        assert getattr(auth_persistence, name) is getattr(runtime_persistence, name)

    assert importlib.util.find_spec("tigrbl_identity_storage.persistence") is None


def test_runtime_owns_consent_and_registration_lifecycle_adapters() -> None:
    runtime = importlib.import_module("tigrbl_identity_storage_runtime")

    assert callable(runtime.record_consent_async)
    assert callable(runtime.revoke_consent_async)
    assert callable(runtime.get_client_registration_async)
    assert callable(runtime.upsert_client_registration_async)


def test_tigrbl_auth_migration_facades_reexport_storage_helpers() -> None:
    auth_migrations = importlib.import_module("tigrbl_auth.migrations")
    auth_runtime = importlib.import_module("tigrbl_auth.migrations.runtime")
    auth_helpers = importlib.import_module("tigrbl_auth.migrations.helpers")
    storage_migrations = importlib.import_module("tigrbl_identity_storage.migrations")
    storage_runtime = importlib.import_module("tigrbl_identity_storage_runtime.migrations.runtime")
    storage_runtime_migrations = importlib.import_module("tigrbl_identity_storage_runtime.migrations")
    storage_helpers = importlib.import_module("tigrbl_identity_storage.migrations.helpers")

    for name in storage_migrations.__all__:
        assert getattr(auth_migrations, name) is getattr(storage_migrations, name)
    for name in storage_runtime_migrations.__all__:
        assert getattr(auth_migrations, name) is getattr(storage_runtime_migrations, name)
    for name in storage_runtime.__all__:
        assert getattr(auth_runtime, name) is getattr(storage_runtime, name)
    for name in storage_helpers.__all__:
        assert getattr(auth_helpers, name) is getattr(storage_helpers, name)


def test_executable_migration_runtime_lives_above_storage() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.migrations.runtime") is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.migrations.runtime")
    assert runtime.VERSIONS_DIR.name == "versions"
    assert "tigrbl-identity-storage" in runtime.VERSIONS_DIR.parts
    assert "tigrbl_identity_storage" in runtime.VERSIONS_DIR.parts


def test_executable_metadata_publishers_live_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.tables.realm._oidc_discovery",
        "tigrbl_identity_storage.tables.realm._oauth_authorization_server_metadata",
        "tigrbl_identity_storage.tables.token_record._protected_resource_metadata",
        "tigrbl_identity_storage.tables.token_record._resource_validation_metadata",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    metadata = importlib.import_module("tigrbl_identity_storage_runtime.metadata")
    assert metadata.include_openid_configuration.__module__ == (
        "tigrbl_identity_storage_runtime.metadata.oidc_discovery"
    )
    assert metadata.include_rfc8414.__module__ == (
        "tigrbl_identity_storage_runtime.metadata.authorization_server_metadata"
    )
    assert metadata.include_rfc9728.__module__ == (
        "tigrbl_identity_storage_runtime.metadata.protected_resource_metadata"
    )
    assert metadata.include_resource_validation_metadata.__module__ == (
        "tigrbl_identity_storage_runtime.metadata.resource_validation_metadata"
    )


def test_executable_revocation_publisher_lives_above_storage() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.revoked_token._route") is None
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.revoked_token._op") is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.revocation")
    lifecycle = importlib.import_module("tigrbl_identity_storage_runtime.token_lifecycle")
    storage = importlib.import_module("tigrbl_identity_storage.tables.revoked_token")

    assert runtime.api is runtime.router
    assert runtime.include_revocation_endpoint.__module__ == "tigrbl_identity_storage_runtime.revocation"
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.revoked_token._ops") is None
    assert runtime.revoke_token_async is lifecycle.revoke_token_async
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")


def test_executable_par_publisher_lives_above_storage() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.pushed_authorization_request._op") is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.par")
    storage = importlib.import_module("tigrbl_identity_storage.tables.pushed_authorization_request")

    assert runtime.api is runtime.router
    assert runtime.include_par_endpoint.__module__ == "tigrbl_identity_storage_runtime.par"
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")


def test_executable_device_authorization_publisher_lives_above_storage() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.device_code._op") is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.device_authorization")
    storage = importlib.import_module("tigrbl_identity_storage.tables.device_code")

    assert runtime.api is runtime.router
    assert runtime.include_device_authorization_endpoint.__module__ == (
        "tigrbl_identity_storage_runtime.device_authorization"
    )
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")


def test_executable_logout_publisher_lives_above_storage() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.logout_state._op") is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.logout")
    storage = importlib.import_module("tigrbl_identity_storage.tables.logout_state")

    assert runtime.api is runtime.router
    assert runtime.include_logout_endpoint.__module__ == "tigrbl_identity_storage_runtime.logout"
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")


def test_executable_client_registration_publisher_lives_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.tables.client_registration._op",
        "tigrbl_identity_storage.tables.client_registration._endpoint",
        "tigrbl_identity_storage.tables.client_registration._route_op",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.client_registration")
    storage = importlib.import_module("tigrbl_identity_storage.tables.client_registration")

    assert runtime.api is runtime.router
    assert runtime.include_client_registration_endpoint.__module__ == (
        "tigrbl_identity_storage_runtime.client_registration"
    )
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")


def test_executable_token_exchange_publisher_lives_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.tables.token_record._token_exchange",
        "tigrbl_identity_storage.tables.token_record._token_exchange_endpoint",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.token_exchange")
    storage = importlib.import_module("tigrbl_identity_storage.tables.token_record")

    assert runtime.api is runtime.router
    assert runtime.include_token_exchange_endpoint.__module__ == (
        "tigrbl_identity_storage_runtime.token_exchange"
    )
    assert not hasattr(storage, "token_exchange")


def test_executable_userinfo_publisher_lives_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.tables.user._oidc_userinfo",
        "tigrbl_identity_storage.tables.user._oidc_userinfo_top",
        "tigrbl_identity_storage.tables.user._rp_userinfo_client",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.userinfo")
    storage = importlib.import_module("tigrbl_identity_storage.tables.user")

    assert runtime.api is runtime.router
    assert runtime.include_oidc_userinfo.__module__ == "tigrbl_identity_storage_runtime.userinfo"
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")
    assert not hasattr(storage, "userinfo")


def test_executable_introspection_publisher_lives_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.tables.token_record._op",
        "tigrbl_identity_storage.tables.token_record._introspection",
        "tigrbl_identity_storage.tables.token_record._introspection_store",
        "tigrbl_identity_storage.tables.token_record._lifecycle",
        "tigrbl_identity_storage.tables.token_record._endpoint",
        "tigrbl_identity_storage.tables.token_record._route",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.introspection")
    storage = importlib.import_module("tigrbl_identity_storage.tables.token_record")

    assert runtime.api is runtime.router
    assert runtime.include_introspection_endpoint.__module__ == (
        "tigrbl_identity_storage_runtime.introspection"
    )
    assert importlib.util.find_spec("tigrbl_identity_storage.tables.token_record._ops") is None
    assert runtime.introspect_token_async.__module__ == (
        "tigrbl_identity_storage_runtime.introspection"
    )
    assert not hasattr(storage, "introspect")
    assert not hasattr(storage, "include_introspection_endpoint")


def test_executable_auth_flow_composition_lives_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.tables.auth_code._authz_surface",
        "tigrbl_identity_storage.tables.auth_code._auth_flows",
        "tigrbl_identity_storage.tables.auth_code._oidc_route",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    authz_surface = importlib.import_module("tigrbl_identity_storage_runtime.authz_surface")
    auth_flows = importlib.import_module("tigrbl_identity_storage_runtime.auth_flows")
    authorization = importlib.import_module("tigrbl_identity_storage_runtime.authorization")

    assert not hasattr(authz_surface, "api")
    assert not hasattr(auth_flows, "api")
    assert not hasattr(authorization, "api")
    assert hasattr(authz_surface, "router")
    assert hasattr(auth_flows, "router")
    assert hasattr(authorization, "router")


def test_executable_account_surface_composition_lives_above_storage() -> None:
    assert importlib.util.find_spec(
        "tigrbl_identity_storage.tables.user._account_surface"
    ) is None

    account_surface = importlib.import_module("tigrbl_auth_api_my_account.routes")

    assert account_surface.api is account_surface.router


def test_operator_service_composition_lives_above_storage() -> None:
    old_modules = (
        "tigrbl_identity_storage.operator_store",
        "tigrbl_identity_storage.resource_service",
        "tigrbl_identity_storage.session_service",
        "tigrbl_identity_storage.audit",
        "tigrbl_identity_storage.portability",
        "tigrbl_identity_storage._operator_store",
        "tigrbl_identity_storage._resource_service",
    )
    for module_name in old_modules:
        assert importlib.util.find_spec(module_name) is None

    runtime_modules = (
        "tigrbl_identity_storage_runtime.operator_store",
        "tigrbl_identity_storage_runtime.resource_service",
        "tigrbl_identity_storage_runtime.session_service",
        "tigrbl_identity_storage_runtime.audit",
        "tigrbl_identity_storage_runtime.portability",
        "tigrbl_identity_storage_runtime._operator_store",
        "tigrbl_identity_storage_runtime._resource_service",
        "tigrbl_identity_storage_runtime.key_management",
    )
    for module_name in runtime_modules:
        assert importlib.import_module(module_name).__name__ == module_name


def test_lower_layers_do_not_import_storage_runtime_composition() -> None:
    lower_layers = (
        Path("pkgs/00-primitives"),
        Path("pkgs/01-storage"),
        Path("pkgs/02-contracts"),
        Path("pkgs/05-bases"),
        Path("pkgs/10-concrete"),
        Path("pkgs/20-providers"),
    )
    offenders: list[str] = []
    for root in lower_layers:
        for path in root.rglob("*.py"):
            if "tigrbl_identity_storage_runtime" in path.read_text(encoding="utf-8"):
                offenders.append(path.as_posix())

    assert offenders == []


def test_token_table_route_does_not_call_sync_session_observer() -> None:
    path = Path(
        "pkgs/01-storage/tigrbl-identity-storage/src/"
        "tigrbl_identity_storage/tables/token_record/_table.py"
    )
    source = path.read_text(encoding="utf-8")

    assert "observe_token_response" not in source
    assert "session_service" not in source


def test_tigrbl_auth_table_modules_do_not_define_duplicate_table_classes() -> None:
    table_dir = Path("pkgs/70-facade/tigrbl-auth/src/tigrbl_auth/tables")
    for path in table_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        class_defs = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert class_defs == [], f"{path} defines duplicate table classes: {class_defs}"


def test_tigrbl_auth_migration_modules_do_not_define_duplicate_runtime_logic() -> None:
    migration_files = [
        Path("pkgs/70-facade/tigrbl-auth/src/tigrbl_auth/migrations/__init__.py"),
    ]
    for path in migration_files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        class_defs = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        function_defs = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        assert class_defs == [], f"{path} defines duplicate migration classes: {class_defs}"
        assert function_defs == [], f"{path} defines duplicate migration functions: {function_defs}"


def test_storage_package_does_not_import_compat_table_facades() -> None:
    storage_root = Path("pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage")
    offenders = []
    for path in storage_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "from tigrbl_auth.tables" in text or "import tigrbl_auth.tables" in text:
            offenders.append(str(path))
    assert offenders == []


def test_storage_migrations_import_canonical_models() -> None:
    migration_root = Path(
        "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/migrations"
    )
    migration_files = list(migration_root.rglob("*.py"))
    assert migration_files
    for path in migration_files:
        text = path.read_text(encoding="utf-8")
        assert "tigrbl_auth.tables" not in text
