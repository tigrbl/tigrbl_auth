"""Executable DDL migration for 0010_realm_namespace_tables."""

from __future__ import annotations

from tigrbl_auth.migrations.helpers import AUTHN_SCHEMA, column_names, create_tables, drop_columns, table_names
from tigrbl_identity_storage.tables import Realm

revision = "0010_realm_namespace_tables"
down_revision = "0009_admin_identity_bootstrap_and_password_recovery"
branch_labels = None
depends_on = None

DEFAULT_REALM_ID = "FFFFFFFF-1000-0000-0000-000000000000"


def _table_name(table: str) -> str:
    return f'"{AUTHN_SCHEMA}"."{table}"'


def _add_column(conn, table: str, ddl: str) -> None:
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(table)} ADD COLUMN {ddl}")


def upgrade(conn) -> None:
    create_tables(conn, Realm)
    if "tenants" in table_names(conn) and "realm_id" not in column_names(conn, "tenants"):
        _add_column(conn, "tenants", "realm_id UUID")


def downgrade(conn) -> None:
    if "tenants" in table_names(conn):
        drop_columns(conn, "tenants", ("realm_id",))
    Realm.__table__.drop(bind=conn, checkfirst=True)
