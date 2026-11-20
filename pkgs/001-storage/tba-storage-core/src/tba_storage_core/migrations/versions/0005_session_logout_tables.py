"""Executable DDL migration for 0005_session_logout_tables."""

from tba_storage_core.migrations.helpers import create_tables, drop_tables
from tba_storage_core.tables import LogoutState

revision = '0005_session_logout_tables'
down_revision = '0004_device_par_revocation_tables'
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, LogoutState)


def downgrade(conn) -> None:
    drop_tables(conn, LogoutState)
