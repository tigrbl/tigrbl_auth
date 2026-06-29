"""Executable DDL migration for durable DPoP replay and nonce state."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables import DpopNonce, DpopReplay

revision = "0023_dpop_replay_nonce_tables"
down_revision = "0022_authority_and_trust_graph_tables"
branch_labels = None
depends_on = None

TABLES = (DpopReplay, DpopNonce)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
