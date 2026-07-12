"""Create credential issuer, configuration, and wallet registry tables."""

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
from tigrbl_identity_storage.tables.credential_ecosystem_registry import (
    CredentialConfiguration,
    CredentialIssuer,
    WalletAttestation,
    WalletInstance,
    WalletKeyBinding,
    WalletRegistration,
)

revision = "0024_credential_issuer_wallet_and_configuration"
down_revision = "0023_artifact_and_token_profile_discriminators"
branch_labels = None
depends_on = None
TABLES = (
    CredentialIssuer,
    CredentialConfiguration,
    WalletRegistration,
    WalletInstance,
    WalletAttestation,
    WalletKeyBinding,
)


def upgrade(conn):
    create_tables(conn, *TABLES)


def downgrade(conn):
    drop_tables(conn, *TABLES)
