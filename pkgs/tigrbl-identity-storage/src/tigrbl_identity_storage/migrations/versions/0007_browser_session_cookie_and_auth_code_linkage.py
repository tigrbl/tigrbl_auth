"""Executable DDL migration for 0007_browser_session_cookie_and_auth_code_linkage."""

from __future__ import annotations

from tigrbl_auth.migrations.helpers import column_names, drop_columns, AUTHN_SCHEMA

revision = '0007_browser_session_cookie_and_auth_code_linkage'
down_revision = '0006_key_rotation_and_audit_tables'
branch_labels = None
depends_on = None

SESSION_COLUMNS = (
    'session_state_salt',
    'cookie_secret_hash',
    'cookie_issued_at',
    'cookie_rotated_at',
)
AUTH_CODE_COLUMNS = ('session_id',)


def _table_name(conn, name: str) -> str:
    return f"{AUTHN_SCHEMA}.{name}"


def _add_column(conn, table: str, ddl: str) -> None:
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(conn, table)} ADD COLUMN {ddl}")


def upgrade(conn) -> None:
    session_cols = column_names(conn, 'sessions')
    if 'session_state_salt' not in session_cols:
        _add_column(conn, 'sessions', 'session_state_salt VARCHAR(128)')
    if 'cookie_secret_hash' not in session_cols:
        _add_column(conn, 'sessions', 'cookie_secret_hash VARCHAR(128)')
    if 'cookie_issued_at' not in session_cols:
        _add_column(conn, 'sessions', 'cookie_issued_at TIMESTAMP')
    if 'cookie_rotated_at' not in session_cols:
        _add_column(conn, 'sessions', 'cookie_rotated_at TIMESTAMP')

    auth_code_cols = column_names(conn, 'auth_codes')
    if 'session_id' not in auth_code_cols:
        if conn.dialect.name == 'sqlite':
            _add_column(conn, 'auth_codes', 'session_id CHAR(32)')
        else:
            _add_column(conn, 'auth_codes', 'session_id UUID')


def downgrade(conn) -> None:
    drop_columns(conn, 'auth_codes', AUTH_CODE_COLUMNS)
    drop_columns(conn, 'sessions', SESSION_COLUMNS)
