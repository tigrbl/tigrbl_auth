"""Executable DDL migration for 0003_authorization_runtime_tables."""

from tigrbl_auth.migrations.helpers import create_tables, drop_tables
from tigrbl_auth.tables import AuthSession, AuthCode, Consent, TokenRecord

revision = '0003_authorization_runtime_tables'
down_revision = '0002_client_and_service_tables'
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, AuthSession, AuthCode, Consent, TokenRecord)


def downgrade(conn) -> None:
    drop_tables(conn, AuthSession, AuthCode, Consent, TokenRecord)
