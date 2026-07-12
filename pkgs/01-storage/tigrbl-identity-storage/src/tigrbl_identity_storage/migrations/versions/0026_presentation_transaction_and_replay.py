"""Create presentation transaction, consent, and replay tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.presentation_state import (
    PresentationConsent,
    PresentationReplay,
    PresentationTransaction,
    VerifierRegistration,
)

revision = "0026_presentation_transaction_and_replay"
down_revision = "0025_credential_issuance_and_status"
branch_labels = None
depends_on = None
TABLES = (
    VerifierRegistration,
    PresentationTransaction,
    PresentationConsent,
    PresentationReplay,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
