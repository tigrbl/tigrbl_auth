"""Executable DDL migration for 0006_key_rotation_and_audit_tables."""

from tigrbl_auth.migrations.helpers import create_tables, drop_tables
from tigrbl_auth.tables import KeyRotationEvent, AuditEvent

revision = '0006_key_rotation_and_audit_tables'
down_revision = '0005_session_logout_tables'
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, KeyRotationEvent, AuditEvent)


def downgrade(conn) -> None:
    drop_tables(conn, KeyRotationEvent, AuditEvent)
