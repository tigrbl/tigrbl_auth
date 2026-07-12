"""Create credential issuance and status lifecycle tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.credential_issuance_state import (
    CredentialDeferredTransaction,
    CredentialIssuanceTransaction,
    CredentialNotification,
    CredentialOffer,
    CredentialStatusEntry,
    CredentialStatusList,
    CredentialStatusPublication,
)

revision = "0025_credential_issuance_and_status"
down_revision = "0024_credential_issuer_wallet_and_configuration"
branch_labels = None
depends_on = None
TABLES = (
    CredentialOffer,
    CredentialIssuanceTransaction,
    CredentialDeferredTransaction,
    CredentialNotification,
    CredentialStatusList,
    CredentialStatusEntry,
    CredentialStatusPublication,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
