"""Concrete RFC 3339 `updated_at` subject-information field."""

from datetime import datetime

from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class UpdatedAtRfc3339Claim(ClaimBase):
    claim_name = "updated_at"
    protocol_label = "rfc9635"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.TIMESTAMP
    default_standards = ("RFC 9635", "RFC 3339")

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str):
            raise ValueError("updated_at must be an RFC 3339 timestamp")
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("updated_at must be an RFC 3339 timestamp") from exc
        if parsed.tzinfo is None:
            raise ValueError("updated_at must include an RFC 3339 offset")


__all__ = ["UpdatedAtRfc3339Claim"]
