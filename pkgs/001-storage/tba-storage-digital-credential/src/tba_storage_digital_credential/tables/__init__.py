"""Owned mapped-table inventory."""

from .credential_ecosystem_registry import CredentialIssuer, CredentialConfiguration, WalletRegistration, WalletInstance, WalletAttestation, WalletKeyBinding
from .credential_issuance_state import CredentialOffer, CredentialIssuanceTransaction, CredentialDeferredTransaction, CredentialNotification, CredentialStatusList, CredentialStatusEntry, CredentialStatusPublication

TABLE_MODELS = (
    CredentialIssuer,
    CredentialConfiguration,
    WalletRegistration,
    WalletInstance,
    WalletAttestation,
    WalletKeyBinding,
    CredentialOffer,
    CredentialIssuanceTransaction,
    CredentialDeferredTransaction,
    CredentialNotification,
    CredentialStatusList,
    CredentialStatusEntry,
    CredentialStatusPublication,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
