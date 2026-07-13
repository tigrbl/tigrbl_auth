"""Create private-claim definition, release-policy, and provenance tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.claim_state import (
    ClaimDefinition,
    ClaimProvenanceRecord,
    ClaimReleasePolicy,
    ClaimSnapshot,
    ClaimSourceBinding,
)

revision = "0032_claim_definition_and_provenance"
down_revision = "0031_certificate_trust_and_status"
branch_labels = None
depends_on = None
TABLES = (
    ClaimDefinition,
    ClaimSourceBinding,
    ClaimReleasePolicy,
    ClaimProvenanceRecord,
    ClaimSnapshot,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
