"""Durable credential lifecycle operations."""

from tigrbl_identity_storage.tables import (
    CredentialIssuanceTransaction,
    CredentialOffer,
    CredentialStatusEntry,
)

from .common import create_table_handler

create_offer = create_table_handler(CredentialOffer)
begin_issuance = create_table_handler(CredentialIssuanceTransaction)
set_credential_status = create_table_handler(CredentialStatusEntry)

__all__ = ["begin_issuance", "create_offer", "set_credential_status"]
