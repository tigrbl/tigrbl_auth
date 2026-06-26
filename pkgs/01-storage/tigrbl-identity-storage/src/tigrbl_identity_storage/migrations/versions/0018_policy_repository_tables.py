"""Executable DDL migration for durable policy repository state."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables import (
    Policy,
    PolicySet,
    PolicySetMember,
    PolicyTarget,
    PolicyVersion,
)

revision = "0018_policy_repository_tables"
down_revision = "0017_authorization_server_table"
branch_labels = None
depends_on = None

TABLES = (Policy, PolicyVersion, PolicySet, PolicySetMember, PolicyTarget)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
