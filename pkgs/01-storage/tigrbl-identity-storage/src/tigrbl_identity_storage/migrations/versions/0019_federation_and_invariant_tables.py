"""Executable DDL migration for federation and invariant table-owned state."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables import (
    AuthorizationInvariant,
    Federation,
    FederatedSession,
    IdentityProvider,
    InvariantEvaluation,
    InvariantViolation,
)

revision = "0019_federation_and_invariant_tables"
down_revision = "0018_policy_tables"
branch_labels = None
depends_on = None

TABLES = (
    IdentityProvider,
    Federation,
    FederatedSession,
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantViolation,
)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
