"""Credential table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    CredentialIssuanceTransaction,
    CredentialOffer,
    CredentialStatusEntry,
)

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.credentials import begin_issuance, create_offer, set_credential_status

CredentialOfferTable = CredentialOffer
CredentialIssuanceTransactionTable = CredentialIssuanceTransaction
CredentialStatusEntryTable = CredentialStatusEntry

CredentialOfferRuntimeSpec = deriveRuntimeTableSpec(
    CredentialOfferTable,
    operations=(makeRuntimeOperation(alias="create_offer", handler=create_offer),),
)
CredentialIssuanceTransactionRuntimeSpec = deriveRuntimeTableSpec(
    CredentialIssuanceTransactionTable,
    operations=(
        makeRuntimeOperation(alias="begin_issuance", handler=begin_issuance),
    ),
)
CredentialStatusEntryRuntimeSpec = deriveRuntimeTableSpec(
    CredentialStatusEntryTable,
    operations=(
        makeRuntimeOperation(
            alias="set_credential_status", handler=set_credential_status
        ),
    ),
)

__all__ = [
    "CredentialIssuanceTransactionRuntimeSpec",
    "CredentialIssuanceTransactionTable",
    "CredentialOfferRuntimeSpec",
    "CredentialOfferTable",
    "CredentialStatusEntryRuntimeSpec",
    "CredentialStatusEntryTable",
]
