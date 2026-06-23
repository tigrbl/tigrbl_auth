"""Executable DDL migration for 0002_client_and_service_tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables import (
    Client,
    ClientRegistration,
    CredentialApiKey,
    CredentialServiceKey,
    ServiceIdentity,
)

revision = '0002_client_and_service_tables'
down_revision = '0001_initial_identity_tables'
branch_labels = None
depends_on = None


def upgrade(conn) -> None:
    create_tables(conn, Client, ClientRegistration, ServiceIdentity, CredentialServiceKey, CredentialApiKey)


def downgrade(conn) -> None:
    drop_tables(conn, Client, ClientRegistration, ServiceIdentity, CredentialServiceKey, CredentialApiKey)
