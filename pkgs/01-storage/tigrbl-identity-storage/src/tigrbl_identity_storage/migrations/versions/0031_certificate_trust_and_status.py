"""Create certificate metadata, trust-anchor, and status-snapshot tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.certificate_state import (
    CertificateRecord,
    CertificateStatusSnapshot,
    TrustAnchor,
)

revision = "0031_certificate_trust_and_status"
down_revision = "0030_optional_did_and_gnap_state"
branch_labels = None
depends_on = None
TABLES = (CertificateRecord, TrustAnchor, CertificateStatusSnapshot)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
