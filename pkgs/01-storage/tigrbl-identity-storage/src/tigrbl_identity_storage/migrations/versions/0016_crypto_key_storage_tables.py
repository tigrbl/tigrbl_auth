"""Executable DDL migration for generic crypto key storage tables."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import column_names, create_tables, drop_tables, ensure_schema, table_names
from tigrbl_identity_storage.tables import (
    CryptoKey,
    CryptoKeyVersion,
    KeyAttestationEvidence,
    KeyEnvelope,
    PrincipalKeyBinding,
)

revision = "0016_crypto_key_storage_tables"
down_revision = "0015_principal_identity_credential_tables"
branch_labels = None
depends_on = None

TABLES = (
    CryptoKey,
    CryptoKeyVersion,
    PrincipalKeyBinding,
    KeyEnvelope,
    KeyAttestationEvidence,
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


def _add_column_if_missing(conn, table: str, ddl: str, column_name: str) -> None:
    if table not in table_names(conn) or column_name in column_names(conn, table):
        return
    conn.exec_driver_sql(f"ALTER TABLE {_table_name(table)} ADD COLUMN {ddl}")


def _adopt_legacy_key_tables(conn) -> None:
    ensure_schema(conn)
    _rename_table_if_present(conn, "identity_keys", "crypto_keys")
    _rename_table_if_present(conn, "identity_key_versions", "crypto_key_versions")
    _rename_column_if_present(conn, "crypto_keys", "public_jwk", "public_material")
    _rename_column_if_present(conn, "crypto_key_versions", "public_jwk", "public_material")

    _add_column_if_missing(conn, "crypto_keys", '"key_kind" VARCHAR(64) NOT NULL DEFAULT \'asymmetric\'', "key_kind")
    _add_column_if_missing(conn, "crypto_keys", '"key_profiles" JSON', "key_profiles")
    _add_column_if_missing(conn, "crypto_keys", '"allowed_ops" JSON', "allowed_ops")
    _add_column_if_missing(conn, "crypto_keys", '"export_policy" VARCHAR(64) NOT NULL DEFAULT \'public_only\'', "export_policy")
    _add_column_if_missing(conn, "crypto_keys", '"origin" VARCHAR(64) NOT NULL DEFAULT \'generated\'', "origin")
    _add_column_if_missing(conn, "crypto_keys", '"extractable" BOOLEAN NOT NULL DEFAULT FALSE', "extractable")
    _add_column_if_missing(conn, "crypto_keys", '"public_material_format" VARCHAR(64)', "public_material_format")
    _add_column_if_missing(conn, "crypto_keys", '"fingerprint" VARCHAR(255)', "fingerprint")

    _add_column_if_missing(conn, "crypto_key_versions", '"allowed_ops" JSON', "allowed_ops")
    _add_column_if_missing(conn, "crypto_key_versions", '"public_material_format" VARCHAR(64)', "public_material_format")
    _add_column_if_missing(conn, "crypto_key_versions", '"fingerprint" VARCHAR(255)', "fingerprint")
    _add_column_if_missing(conn, "crypto_key_versions", '"not_before" TIMESTAMP', "not_before")
    _add_column_if_missing(conn, "crypto_key_versions", '"not_after" TIMESTAMP', "not_after")
    _add_column_if_missing(conn, "crypto_key_versions", '"activated_at" TIMESTAMP', "activated_at")
    _add_column_if_missing(conn, "crypto_key_versions", '"retired_at" TIMESTAMP', "retired_at")


def upgrade(conn) -> None:
    _adopt_legacy_key_tables(conn)
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, KeyAttestationEvidence, KeyEnvelope, PrincipalKeyBinding)
