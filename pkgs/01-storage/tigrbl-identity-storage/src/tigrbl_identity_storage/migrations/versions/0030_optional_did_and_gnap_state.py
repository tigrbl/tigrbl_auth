"""Create optional DID and GNAP durable state tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.did_gnap_state import (
    DidDocument,
    DidDocumentVersion,
    DidResolutionCache,
    DidService,
    DidVerificationMethod,
    GnapClientInstance,
    GnapContinuation,
    GnapGrant,
    GnapInteraction,
)

revision = "0030_optional_did_and_gnap_state"
down_revision = "0029_security_event_delivery"
branch_labels = None
depends_on = None
TABLES = (
    DidDocument,
    DidDocumentVersion,
    DidVerificationMethod,
    DidService,
    DidResolutionCache,
    GnapGrant,
    GnapContinuation,
    GnapClientInstance,
    GnapInteraction,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
