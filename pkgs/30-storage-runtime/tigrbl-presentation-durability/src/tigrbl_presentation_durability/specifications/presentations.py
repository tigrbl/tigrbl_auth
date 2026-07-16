"""Presentation table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    PresentationConsent,
    PresentationReplay,
    PresentationTransaction,
)

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_presentation_durability.operations.presentations import (
    begin_presentation,
    record_presentation_consent,
    reserve_presentation_replay,
)

PresentationTransactionTable = PresentationTransaction
PresentationConsentTable = PresentationConsent
PresentationReplayTable = PresentationReplay

PresentationTransactionRuntimeSpec = deriveRuntimeTableSpec(
    PresentationTransactionTable,
    operations=(
        makeRuntimeOperation(alias="begin_presentation", handler=begin_presentation),
    ),
)
PresentationConsentRuntimeSpec = deriveRuntimeTableSpec(
    PresentationConsentTable,
    operations=(
        makeRuntimeOperation(
            alias="record_consent", handler=record_presentation_consent
        ),
    ),
)
PresentationReplayRuntimeSpec = deriveRuntimeTableSpec(
    PresentationReplayTable,
    operations=(
        makeRuntimeOperation(
            alias="reserve_replay", handler=reserve_presentation_replay
        ),
    ),
)

__all__ = [
    "PresentationConsentRuntimeSpec",
    "PresentationConsentTable",
    "PresentationReplayRuntimeSpec",
    "PresentationReplayTable",
    "PresentationTransactionRuntimeSpec",
    "PresentationTransactionTable",
]
