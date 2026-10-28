"""Executable DDL migration for 0001_initial_identity_tables."""

from tba_storage_core.migrations.helpers import create_tables, drop_tables
from tba_storage_core.tables import Realm, Tenant, User

revision = '0001_initial_identity_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, Realm, Tenant, User)


def downgrade(conn) -> None:
    drop_tables(conn, Realm, Tenant, User)
