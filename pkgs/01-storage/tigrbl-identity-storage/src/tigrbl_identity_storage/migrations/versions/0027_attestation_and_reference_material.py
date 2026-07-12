"""Create attestation evidence, appraisal, and reference-material tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.attestation_state import (
    AttestationAppraisalPolicy,
    AttestationEndorsement,
    AttestationEvidence,
    AttestationReferenceManifest,
    AttestationReferenceValue,
    AttestationResult,
)

revision = "0027_attestation_and_reference_material"
down_revision = "0026_presentation_transaction_and_replay"
branch_labels = None
depends_on = None
TABLES = (
    AttestationEvidence,
    AttestationResult,
    AttestationReferenceManifest,
    AttestationReferenceValue,
    AttestationEndorsement,
    AttestationAppraisalPolicy,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
