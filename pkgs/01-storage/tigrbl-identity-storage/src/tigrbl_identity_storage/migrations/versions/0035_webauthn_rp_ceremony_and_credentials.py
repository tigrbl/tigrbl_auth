"""Add durable WebAuthn relying-party, ceremony, credential, and attestation state."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import (
    AUTHN_SCHEMA,
    column_names,
    create_tables,
    drop_columns,
    drop_tables,
)
from tigrbl_identity_storage.tables import (
    CredentialWebAuthnPasskey,
    WebAuthnAttestationRecord,
    WebAuthnCeremony,
    WebAuthnRelyingParty,
)

revision = "0035_webauthn_rp_ceremony_and_credentials"
down_revision = "0034_dpop_replay_nonce_tables"
branch_labels = None
depends_on = None

NEW_TABLES = (WebAuthnRelyingParty, WebAuthnCeremony, WebAuthnAttestationRecord)

CREDENTIAL_COLUMNS = (
    ("credential_external_id", "credential_external_id VARCHAR(1000)"),
    ("credential_public_key_cose", "credential_public_key_cose BLOB"),
    ("user_handle", "user_handle BLOB"),
    ("cose_algorithm", "cose_algorithm INTEGER"),
    ("aaguid", "aaguid BLOB"),
    ("attestation_format", "attestation_format VARCHAR(64)"),
    ("attestation_type", "attestation_type VARCHAR(64)"),
    ("attestation_trust_status", "attestation_trust_status VARCHAR(32)"),
    ("discoverable", "discoverable BOOLEAN NOT NULL DEFAULT FALSE"),
    ("backup_eligible", "backup_eligible BOOLEAN NOT NULL DEFAULT FALSE"),
    ("backup_state", "backup_state BOOLEAN NOT NULL DEFAULT FALSE"),
    ("last_used_at", "last_used_at TIMESTAMP"),
    ("revoked_at", "revoked_at TIMESTAMP"),
    ("display_name", "display_name VARCHAR(255)"),
)


def _table(conn, name: str) -> str:
    return f'"{AUTHN_SCHEMA}"."{name}"'


def _binary_ddl(conn, ddl: str) -> str:
    if conn.dialect.name == "postgresql":
        return ddl.replace(" BLOB", " BYTEA")
    return ddl


def upgrade(conn) -> None:
    create_tables(conn, *NEW_TABLES)
    table = CredentialWebAuthnPasskey.__tablename__
    existing = column_names(conn, table)
    for name, ddl in CREDENTIAL_COLUMNS:
        if name not in existing:
            conn.exec_driver_sql(
                f"ALTER TABLE {_table(conn, table)} ADD COLUMN {_binary_ddl(conn, ddl)}"
            )
    conn.exec_driver_sql(
        f"UPDATE {_table(conn, table)} "
        "SET credential_external_id = webauthn_credential_id "
        "WHERE credential_external_id IS NULL"
    )


def downgrade(conn) -> None:
    drop_columns(
        conn,
        CredentialWebAuthnPasskey.__tablename__,
        [name for name, _ in CREDENTIAL_COLUMNS],
    )
    drop_tables(conn, *NEW_TABLES)
