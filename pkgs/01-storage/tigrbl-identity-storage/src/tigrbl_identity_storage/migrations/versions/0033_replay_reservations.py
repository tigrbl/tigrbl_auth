"""Create protocol-neutral atomic replay reservation state."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.replay_reservation import ReplayReservation

revision = "0033_replay_reservations"
down_revision = "0032_claim_definition_and_provenance"
branch_labels = None
depends_on = None
TABLES = (ReplayReservation,)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
