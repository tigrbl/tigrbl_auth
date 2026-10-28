"""Executable DDL migration for authority and trust graph tables."""

from __future__ import annotations

from tba_storage_core.migrations.helpers import create_tables, drop_tables
from tba_storage_core.tables import (
    AuthorityDerivationGraph,
    AuthorityDerivationGraphEdge,
    AuthorityDerivationGraphNode,
    TrustFederationGraph,
    TrustFederationGraphEdge,
    TrustFederationGraphNode,
)

revision = "0022_authority_and_trust_graph_tables"
down_revision = "0021_authentication_challenge_table"
branch_labels = None
depends_on = None

TABLES = (
    AuthorityDerivationGraph,
    AuthorityDerivationGraphNode,
    AuthorityDerivationGraphEdge,
    TrustFederationGraph,
    TrustFederationGraphNode,
    TrustFederationGraphEdge,
)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
