from __future__ import annotations

import ast
import importlib
import importlib.util
from pathlib import Path


TABLE_MODULE_EXPORTS = {
    "access_review_campaign": ("AccessReviewCampaign",),
    "access_review_decision": ("AccessReviewDecision",),
    "access_review_item": ("AccessReviewItem",),
    "api_key": ("ApiKey",),
    "attribute_policy": ("AttributePolicy",),
    "audit_event": ("AuditEvent",),
    "auth_code": ("AuthCode",),
    "auth_session": ("AuthSession",),
    "client": ("Client", "_CLIENT_ID_RE"),
    "client_registration": ("ClientRegistration",),
    "consent": ("Consent",),
    "credential": ("Credential",),
    "credential_audit_event": ("CredentialAuditEvent",),
    "credential_dpop_key": ("CredentialDpopKey",),
    "credential_mtls_certificate": ("CredentialMtlsCertificate",),
    "device_code": ("DeviceCode",),
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
    "key": ("Key",),
    "key_rotation_event": ("KeyRotationEvent",),
    "key_rotation_policy": ("KeyRotationPolicy",),
    "key_version": ("KeyVersion",),
    "logout_state": ("LogoutState",),
    "pushed_authorization_request": (
        "PushedAuthorizationRequest",
        "DEFAULT_PAR_EXPIRY",
    ),
    "realm": ("Realm",),
    "revoked_token": ("RevokedToken",),
    "residency_zone": ("ResidencyZone",),
    "role": ("Role",),
    "service": ("Service",),
    "service_key": ("ServiceKey",),
    "subject_alias": ("SubjectAlias",),
    "tenant": ("Tenant",),
    "tenant_membership": ("TenantMembership",),
    "tenant_residency": ("TenantResidency",),
    "token_record": ("TokenRecord",),
    "user": ("User",),
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


def test_tigrbl_auth_tables_and_db_facades_reexport_storage_symbols() -> None:
    auth_tables = importlib.import_module("tigrbl_auth.tables")
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    auth_db = importlib.import_module("tigrbl_auth.db")
    storage_db = importlib.import_module("tigrbl_identity_storage.db")

    for name in storage_tables.__all__:
        assert getattr(auth_tables, name) is getattr(storage_tables, name)

    assert auth_db.ENGINE is storage_db.ENGINE
    assert auth_db.dsn == storage_db.dsn
    assert auth_db.get_db is storage_db.get_db

    auth_realm = importlib.import_module("tigrbl_auth.tables.realm")
    storage_realm = importlib.import_module("tigrbl_identity_storage.tables.realm")
    assert auth_realm.Realm is storage_realm.Realm


def test_orm_export_paths_are_not_supported() -> None:
    assert importlib.util.find_spec("tigrbl_auth.orm") is None
    assert importlib.util.find_spec("tigrbl_identity_storage.orm") is None


def test_tigrbl_auth_persistence_facade_reexports_storage_helpers() -> None:
    auth_persistence = importlib.import_module("tigrbl_auth.services.persistence")
    storage_persistence = importlib.import_module("tigrbl_identity_storage.persistence")

    for name in storage_persistence.__all__:
        assert getattr(auth_persistence, name) is getattr(storage_persistence, name)


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

    runtime = importlib.import_module("tigrbl_identity_storage_runtime.revocation")
    storage = importlib.import_module("tigrbl_identity_storage.tables.revoked_token")
    storage_ops = importlib.import_module("tigrbl_identity_storage.tables.revoked_token._op")

    assert runtime.api is runtime.router
    assert runtime.include_revocation_endpoint.__module__ == "tigrbl_identity_storage_runtime.revocation"
    assert runtime.revoke_token_async is storage_ops.revoke_token_async
    assert not hasattr(storage, "api")
    assert not hasattr(storage, "router")


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
