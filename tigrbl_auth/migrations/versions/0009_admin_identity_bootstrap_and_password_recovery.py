"""Executable DDL migration for 0009_admin_identity_bootstrap_and_password_recovery."""

from __future__ import annotations

from tigrbl_auth.migrations.helpers import AUTHN_SCHEMA, column_names, drop_columns

revision = "0009_admin_identity_bootstrap_and_password_recovery"
down_revision = "0008_refresh_token_family_state"
branch_labels = None
depends_on = None

USER_COLUMNS = (
    "is_admin",
    "is_superuser",
    "must_change_password",
    "password_reset_token_hash",
    "password_reset_expires_at",
)


def _table_name(name: str) -> str:
    return f"{AUTHN_SCHEMA}.{name}"


def _add_column(conn, table: str, ddl: str) -> None:
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(table)} ADD COLUMN {ddl}")


def upgrade(conn) -> None:
    user_cols = column_names(conn, "users")
    if "is_admin" not in user_cols:
        _add_column(conn, "users", "is_admin BOOLEAN NOT NULL DEFAULT 0")
    if "is_superuser" not in user_cols:
        _add_column(conn, "users", "is_superuser BOOLEAN NOT NULL DEFAULT 0")
    if "must_change_password" not in user_cols:
        _add_column(conn, "users", "must_change_password BOOLEAN NOT NULL DEFAULT 0")
    if "password_reset_token_hash" not in user_cols:
        _add_column(conn, "users", "password_reset_token_hash VARCHAR(128)")
    if "password_reset_expires_at" not in user_cols:
        _add_column(conn, "users", "password_reset_expires_at TIMESTAMP")


def downgrade(conn) -> None:
    drop_columns(conn, "users", USER_COLUMNS)
