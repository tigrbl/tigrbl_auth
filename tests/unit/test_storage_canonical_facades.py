from __future__ import annotations

import ast
import importlib
from pathlib import Path


TABLE_MODULE_EXPORTS = {
    "api_key": ("ApiKey",),
    "audit_event": ("AuditEvent",),
    "auth_code": ("AuthCode",),
    "auth_session": ("AuthSession",),
    "client": ("Client", "_CLIENT_ID_RE"),
    "client_registration": ("ClientRegistration",),
    "consent": ("Consent",),
    "device_code": ("DeviceCode",),
    "delegation_grant": (
        "DelegationGrantRecord",
        "DelegationGrantScope",
        "DelegationGrantProof",
        "DelegationGrantEdge",
        "DelegationGrantTokenLink",
    ),
    "key_rotation_event": ("KeyRotationEvent",),
    "logout_state": ("LogoutState",),
    "pushed_authorization_request": (
        "PushedAuthorizationRequest",
        "DEFAULT_PAR_EXPIRY",
    ),
    "realm": ("Realm",),
    "revoked_token": ("RevokedToken",),
    "service": ("Service",),
    "service_key": ("ServiceKey",),
    "tenant": ("Tenant",),
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


def test_tigrbl_auth_orm_and_db_facades_reexport_storage_symbols() -> None:
    auth_orm = importlib.import_module("tigrbl_auth.orm")
    storage_orm = importlib.import_module("tigrbl_identity_storage.orm")
    auth_db = importlib.import_module("tigrbl_auth.db")
    storage_db = importlib.import_module("tigrbl_identity_storage.db")

    for name in storage_orm.__all__:
        assert getattr(auth_orm, name) is getattr(storage_orm, name)

    assert auth_db.ENGINE is storage_db.ENGINE
    assert auth_db.dsn == storage_db.dsn
    assert auth_db.get_db is storage_db.get_db

    auth_realm = importlib.import_module("tigrbl_auth.orm.realm")
    storage_realm = importlib.import_module("tigrbl_identity_storage.orm.realm")
    assert auth_realm.Realm is storage_realm.Realm


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
    storage_runtime = importlib.import_module("tigrbl_identity_storage.migrations.runtime")
    storage_helpers = importlib.import_module("tigrbl_identity_storage.migrations.helpers")

    for name in storage_migrations.__all__:
        assert getattr(auth_migrations, name) is getattr(storage_migrations, name)
    for name in storage_runtime.__all__:
        assert getattr(auth_runtime, name) is getattr(storage_runtime, name)
    for name in storage_helpers.__all__:
        assert getattr(auth_helpers, name) is getattr(storage_helpers, name)


def test_tigrbl_auth_table_modules_do_not_define_duplicate_table_classes() -> None:
    table_dir = Path("pkgs/tigrbl-auth/src/tigrbl_auth/tables")
    for path in table_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        class_defs = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        assert class_defs == [], f"{path} defines duplicate table classes: {class_defs}"


def test_tigrbl_auth_migration_modules_do_not_define_duplicate_runtime_logic() -> None:
    migration_files = [
        Path("pkgs/tigrbl-auth/src/tigrbl_auth/migrations/__init__.py"),
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
    storage_root = Path("pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage")
    offenders = []
    for path in storage_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "from tigrbl_auth.tables" in text or "import tigrbl_auth.tables" in text:
            offenders.append(str(path))
    assert offenders == []


def test_storage_migrations_import_canonical_models() -> None:
    migration_root = Path(
        "pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage/migrations"
    )
    migration_files = list(migration_root.rglob("*.py"))
    assert migration_files
    for path in migration_files:
        text = path.read_text(encoding="utf-8")
        assert "tigrbl_auth.tables" not in text
