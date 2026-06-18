"""Compatibility facade for canonical identity-storage migration helpers."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.migrations.helpers import (
    AUTHN_SCHEMA,
    MIGRATION_TABLE,
    applied_revisions,
    column_names,
    create_tables,
    drop_columns,
    drop_tables,
    ensure_migration_table,
    ensure_schema,
    mark_revision,
    table_names,
    unmark_revision,
)

__all__ = [
    "AUTHN_SCHEMA",
    "MIGRATION_TABLE",
    "applied_revisions",
    "column_names",
    "create_tables",
    "drop_columns",
    "drop_tables",
    "ensure_migration_table",
    "ensure_schema",
    "mark_revision",
    "table_names",
    "unmark_revision",
]
