"""Executable DDL migration for DelegationGrant lifecycle tables."""

from __future__ import annotations

from tigrbl_auth._identity_storage import ensure_identity_storage_importable
from tigrbl_auth.migrations.helpers import create_tables, drop_tables

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables import (
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantRecord,
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
        DelegationGrantRecord,
        DelegationGrantScope,
        DelegationGrantProof,
        DelegationGrantEdge,
        DelegationGrantTokenLink,
    )


def downgrade(conn) -> None:
    drop_tables(
        conn,
        DelegationGrantRecord,
        DelegationGrantScope,
        DelegationGrantProof,
        DelegationGrantEdge,
        DelegationGrantTokenLink,
    )
