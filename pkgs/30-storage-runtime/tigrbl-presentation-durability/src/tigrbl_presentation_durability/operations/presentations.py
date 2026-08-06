"""Durable presentation lifecycle operations."""

from tigrbl_identity_core.persistence import reject_sensitive_raw_fields
from tigrbl_identity_storage.tables import (
    PresentationConsent,
    PresentationReplay,
    PresentationTransaction,
)

from tigrbl import provideTableHandler

begin_presentation = provideTableHandler(
    PresentationTransaction, payload_validator=reject_sensitive_raw_fields
)
record_presentation_consent = provideTableHandler(
    PresentationConsent, payload_validator=reject_sensitive_raw_fields
)
reserve_presentation_replay = provideTableHandler(
    PresentationReplay, payload_validator=reject_sensitive_raw_fields
)

__all__ = [
    "begin_presentation",
    "record_presentation_consent",
    "reserve_presentation_replay",
]
