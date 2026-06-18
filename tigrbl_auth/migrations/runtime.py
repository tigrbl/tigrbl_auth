"""Compatibility facade for canonical identity-storage migration runtime."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.migrations.runtime import (
    MigrationResult,
    SchemaVerification,
    apply_all_async,
    column_names_async,
    column_names_sync,
    downgrade_one_async,
    expected_table_names,
    iter_migration_modules,
    verify_schema_async,
    verify_schema_sync,
)

__all__ = [
    "MigrationResult",
    "SchemaVerification",
    "apply_all_async",
    "column_names_async",
    "column_names_sync",
    "downgrade_one_async",
    "expected_table_names",
    "iter_migration_modules",
    "verify_schema_async",
    "verify_schema_sync",
]
