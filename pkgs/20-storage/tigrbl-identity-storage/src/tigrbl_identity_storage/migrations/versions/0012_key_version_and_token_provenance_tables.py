"""Executable DDL migration for key versions and token provenance."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import AUTHN_SCHEMA, column_names, create_tables, drop_columns, drop_tables
from tigrbl_identity_storage.tables import Key, KeyVersion

revision = "0012_key_version_and_token_provenance_tables"
down_revision = "0011_delegation_grant_lifecycle_tables"
branch_labels = None
depends_on = None


def _table_name(conn, table: str) -> str:
    return f'"{AUTHN_SCHEMA}"."{table}"'


def _add_column_if_missing(conn, table: str, name: str, ddl: str) -> None:
    if name in column_names(conn, table):
        return
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(conn, table)} ADD COLUMN {ddl}")


def upgrade(conn) -> None:
    create_tables(conn, Key, KeyVersion)
    _add_column_if_missing(conn, "token_records", "jti", '"jti" VARCHAR(128)')
    _add_column_if_missing(conn, "token_records", "token_status", '"token_status" VARCHAR(32) NOT NULL DEFAULT \'active\'')
    _add_column_if_missing(conn, "token_records", "kid", '"kid" VARCHAR(255)')
    _add_column_if_missing(conn, "token_records", "key_version", '"key_version" INTEGER')
    _add_column_if_missing(conn, "revoked_tokens", "refresh_family_id", '"refresh_family_id" VARCHAR(64)')


def downgrade(conn) -> None:
    drop_columns(conn, "revoked_tokens", ("refresh_family_id",))
    drop_columns(conn, "token_records", ("jti", "token_status", "kid", "key_version"))
    drop_tables(conn, Key, KeyVersion)
