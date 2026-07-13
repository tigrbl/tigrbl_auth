from tigrbl_identity_storage.tables.presentation_consent import PresentationConsent
from tigrbl_identity_storage.tables.presentation_replay import PresentationReplay
from tigrbl_identity_storage.tables.presentation_transaction import (
    PresentationTransaction,
)

from .repositories import DurableRepository


class PresentationTransactionRepository(DurableRepository):
    table = PresentationTransaction


class PresentationConsentRepository(DurableRepository):
    table = PresentationConsent


class PresentationReplayRepository(DurableRepository):
    table = PresentationReplay


__all__ = [
    "PresentationConsentRepository",
    "PresentationReplayRepository",
    "PresentationTransactionRepository",
]
