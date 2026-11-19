"""Executable DDL migration for DelegationGrant lifecycle tables."""

from __future__ import annotations

from tba_storage_core.migrations.helpers import create_tables, drop_tables
from tba_storage_core.tables import (
    DelegationGrant,
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantScope,
    DelegationGrantTokenLink,
)

revision = "0011_delegation_grant_lifecycle_tables"
down_revision = "0010_realm_namespace_tables"
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(
        conn,
        DelegationGrant,
        DelegationGrantScope,
        DelegationGrantProof,
        DelegationGrantEdge,
        DelegationGrantTokenLink,
    )


def downgrade(conn) -> None:
    drop_tables(
        conn,
        DelegationGrant,
        DelegationGrantScope,
        DelegationGrantProof,
        DelegationGrantEdge,
        DelegationGrantTokenLink,
    )
