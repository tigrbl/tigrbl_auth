"""Durable presentation lifecycle operations."""

from tigrbl_identity_storage.tables import (
    PresentationConsent,
    PresentationReplay,
    PresentationTransaction,
)

from tigrbl_table_durability import create_table_handler

begin_presentation = create_table_handler(PresentationTransaction)
record_presentation_consent = create_table_handler(PresentationConsent)
reserve_presentation_replay = create_table_handler(PresentationReplay)

__all__ = [
    "begin_presentation",
    "record_presentation_consent",
    "reserve_presentation_replay",
]
