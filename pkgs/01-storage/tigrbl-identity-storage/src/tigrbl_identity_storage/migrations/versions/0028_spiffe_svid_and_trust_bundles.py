"""Create SPIFFE SVID and trust-bundle metadata tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.spiffe_state import (
    SpiffeTrustBundle,
    SvidRecord,
    TrustDomainFederation,
)

revision = "0028_spiffe_svid_and_trust_bundles"
down_revision = "0027_attestation_and_reference_material"
branch_labels = None
depends_on = None
TABLES = (SvidRecord, SpiffeTrustBundle, TrustDomainFederation)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
