from tigrbl_identity_storage.tables.credential_issuance_transaction import (
    CredentialIssuanceTransaction,
)
from tigrbl_identity_storage.tables.credential_offer import CredentialOffer
from tigrbl_identity_storage.tables.credential_status_entry import CredentialStatusEntry

from .repositories import DurableRepository


class CredentialOfferRepository(DurableRepository):
    table = CredentialOffer


class CredentialIssuanceTransactionRepository(DurableRepository):
    table = CredentialIssuanceTransaction


class CredentialStatusEntryRepository(DurableRepository):
    table = CredentialStatusEntry


__all__ = [
    "CredentialIssuanceTransactionRepository",
    "CredentialOfferRepository",
    "CredentialStatusEntryRepository",
]
