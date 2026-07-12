"""Add digital-artifact and explicit token-profile discriminators."""

from tigrbl_identity_storage.migrations.helpers import (
    AUTHN_SCHEMA,
    column_names,
    drop_columns,
)

revision = "0023_artifact_and_token_profile_discriminators"
down_revision = "0022_authority_and_trust_graph_tables"
branch_labels = None
depends_on = None

GROUPS = {
    "credentials": (
        ("format", "format VARCHAR(64)"),
        ("credential_type", "credential_type VARCHAR(255)"),
        ("issuer_id", "issuer_id VARCHAR(255)"),
        ("subject_id", "subject_id VARCHAR(255)"),
        ("holder_binding_kind", "holder_binding_kind VARCHAR(64)"),
        ("status_reference", "status_reference VARCHAR(1000)"),
        ("payload_digest", "payload_digest VARCHAR(128)"),
        ("issued_at", "issued_at TIMESTAMP"),
        ("valid_from", "valid_from TIMESTAMP"),
        ("valid_until", "valid_until TIMESTAMP"),
    ),
    "token_records": (
        ("token_profile", "token_profile VARCHAR(128)"),
        ("audience_digest", "audience_digest VARCHAR(128)"),
        ("sender_constraint_kind", "sender_constraint_kind VARCHAR(64)"),
        ("credential_or_grant_reference", "credential_or_grant_reference VARCHAR(255)"),
    ),
    "workload_identities": (
        ("spiffe_id", "spiffe_id VARCHAR(1000)"),
        ("selector_digest", "selector_digest VARCHAR(128)"),
        ("svid_type", "svid_type VARCHAR(32)"),
        ("bundle_version", "bundle_version VARCHAR(128)"),
    ),
    "key_attestation_evidence": (
        ("profile", "profile VARCHAR(255)"),
        ("issuer", "issuer VARCHAR(1000)"),
        ("evidence_digest", "evidence_digest VARCHAR(128)"),
        ("verification_result", "verification_result VARCHAR(64)"),
        ("valid_until", "valid_until TIMESTAMP"),
    ),
}


def _table(conn, name: str) -> str:
    return f'"{AUTHN_SCHEMA}"."{name}"'


def upgrade(conn) -> None:
    for table, columns in GROUPS.items():
        existing = column_names(conn, table)
        for name, ddl in columns:
            if name not in existing:
                conn.exec_driver_sql(
                    f"ALTER TABLE {_table(conn, table)} ADD COLUMN {ddl}"
                )


def downgrade(conn) -> None:
    for table, columns in reversed(tuple(GROUPS.items())):
        drop_columns(conn, table, tuple(name for name, _ in columns))
