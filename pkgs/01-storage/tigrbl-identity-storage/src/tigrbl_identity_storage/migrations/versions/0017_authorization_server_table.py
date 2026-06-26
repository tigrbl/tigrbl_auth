"""Executable DDL migration for durable authorization-server state."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables import AuthorizationServer

revision = "0017_authorization_server_table"
down_revision = "0016_crypto_key_storage_tables"
branch_labels = None
depends_on = None

TABLES = (AuthorizationServer,)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
