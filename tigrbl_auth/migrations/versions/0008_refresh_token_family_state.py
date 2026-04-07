"""Executable DDL migration for 0008_refresh_token_family_state."""

from __future__ import annotations

from tigrbl_auth.migrations.helpers import AUTHN_SCHEMA, column_names, drop_columns

revision = "0008_refresh_token_family_state"
down_revision = "0007_browser_session_cookie_and_auth_code_linkage"
branch_labels = None
depends_on = None

TOKEN_RECORD_COLUMNS = (
    "refresh_family_id",
    "refresh_parent_hash",
    "refresh_successor_hash",
    "used_at",
    "reuse_detected_at",
)


def _table_name(conn, name: str) -> str:
    return name if conn.dialect.name == "sqlite" else f"{AUTHN_SCHEMA}.{name}"


def _add_column(conn, table: str, ddl: str) -> None:
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(conn, table)} ADD COLUMN {ddl}")


def upgrade(conn) -> None:
    token_cols = column_names(conn, "token_records")
    if "refresh_family_id" not in token_cols:
        _add_column(conn, "token_records", "refresh_family_id VARCHAR(64)")
    if "refresh_parent_hash" not in token_cols:
        _add_column(conn, "token_records", "refresh_parent_hash VARCHAR(128)")
    if "refresh_successor_hash" not in token_cols:
        _add_column(conn, "token_records", "refresh_successor_hash VARCHAR(128)")
    if "used_at" not in token_cols:
        _add_column(conn, "token_records", "used_at TIMESTAMP")
    if "reuse_detected_at" not in token_cols:
        _add_column(conn, "token_records", "reuse_detected_at TIMESTAMP")


def downgrade(conn) -> None:
    drop_columns(conn, "token_records", TOKEN_RECORD_COLUMNS)
