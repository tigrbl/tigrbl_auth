"""Executable DDL migration for principal, identity, and credential subtype tables."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import column_names, create_tables, drop_tables, ensure_schema, table_names
from tigrbl_identity_storage.tables import (
    CredentialApiKey,
    CredentialClientSecret,
    CredentialMfaFactor,
    CredentialPassword,
    CredentialRecoveryCode,
    CredentialServiceKey,
    CredentialWebAuthnPasskey,
    MachineIdentity,
    Principal,
    ServiceIdentity,
    WorkloadIdentity,
)

revision = "0015_principal_identity_credential_tables"
down_revision = "0014_optional_contract_state_tables"
branch_labels = None
depends_on = None

TABLES = (
    Principal,
    ServiceIdentity,
    MachineIdentity,
    WorkloadIdentity,
    CredentialApiKey,
    CredentialServiceKey,
    CredentialPassword,
    CredentialClientSecret,
    CredentialWebAuthnPasskey,
    CredentialMfaFactor,
    CredentialRecoveryCode,
)


def _table_name(table: str) -> str:
    return f'"authn"."{table}"'


def _rename_table_if_present(conn, old: str, new: str) -> None:
    names = table_names(conn)
    if old not in names or new in names:
        return
    conn.exec_driver_sql(f'ALTER TABLE {_table_name(old)} RENAME TO "{new}"')


def _rename_column_if_present(conn, table: str, old: str, new: str) -> None:
    columns = column_names(conn, table)
    if old not in columns or new in columns:
        return
    conn.exec_driver_sql(f'ALTER TABLE {_table_name(table)} RENAME COLUMN "{old}" TO "{new}"')


def _add_column_if_missing(conn, table: str, column_sql: str, column_name: str) -> None:
    if table not in table_names(conn) or column_name in column_names(conn, table):
        return
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(table)} ADD COLUMN {column_sql}")


def _adopt_legacy_identity_credential_tables(conn) -> None:
    ensure_schema(conn)
    _rename_table_if_present(conn, "services", "service_identities")
    _rename_table_if_present(conn, "service_keys", "credential_service_keys")
    _rename_table_if_present(conn, "api_keys", "credential_api_keys")
    _rename_column_if_present(conn, "credential_service_keys", "service_id", "service_identity_id")
    _rename_column_if_present(conn, "credential_api_keys", "user_id", "principal_id")
    _add_column_if_missing(
        conn,
        "credential_api_keys",
        '"principal_kind" VARCHAR(64) NOT NULL DEFAULT \'user\'',
        "principal_kind",
    )


def upgrade(conn) -> None:
    _adopt_legacy_identity_credential_tables(conn)
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
