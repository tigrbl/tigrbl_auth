"""Executable DDL migration for durable DPoP replay and nonce state."""

from __future__ import annotations

from tba_storage_core.migrations.helpers import create_tables, drop_tables
from tba_storage_core.tables import DpopNonce, DpopReplay

revision = "0034_dpop_replay_nonce_tables"
down_revision = "0033_replay_reservations"
branch_labels = None
depends_on = None

TABLES = (DpopReplay, DpopNonce)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
