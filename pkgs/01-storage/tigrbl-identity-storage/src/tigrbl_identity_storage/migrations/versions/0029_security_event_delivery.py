"""Create security-event delivery and replay tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.security_event_state import (
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
    SecurityEventSubscription,
)

revision = "0029_security_event_delivery"
down_revision = "0028_spiffe_svid_and_trust_bundles"
branch_labels = None
depends_on = None
TABLES = (
    SecurityEvent,
    SecurityEventSubscription,
    SecurityEventDelivery,
    SecurityEventReplay,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
