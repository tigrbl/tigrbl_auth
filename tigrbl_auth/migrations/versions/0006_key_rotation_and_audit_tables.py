"""Executable DDL migration for 0006_key_rotation_and_audit_tables."""

from tigrbl_auth.migrations.helpers import create_tables, drop_tables
from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables import KeyRotationEvent, AuditEvent

revision = '0006_key_rotation_and_audit_tables'
down_revision = '0005_session_logout_tables'
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, KeyRotationEvent, AuditEvent)


def downgrade(conn) -> None:
    drop_tables(conn, KeyRotationEvent, AuditEvent)
