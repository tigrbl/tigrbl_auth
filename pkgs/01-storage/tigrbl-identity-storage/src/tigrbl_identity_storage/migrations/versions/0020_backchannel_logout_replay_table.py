"""Executable DDL migration for OIDC back-channel logout replay state."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables import BackchannelLogoutReplay

revision = "0020_backchannel_logout_replay_table"
down_revision = "0019_federation_and_invariant_tables"
branch_labels = None
depends_on = None

TABLES = (BackchannelLogoutReplay,)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
