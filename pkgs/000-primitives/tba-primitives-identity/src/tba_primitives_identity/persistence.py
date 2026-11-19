"""Identity persistence boundary guards."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

SENSITIVE_RAW_FIELDS = frozenset(
    {"raw_nonce", "pre_authorized_code", "presentation_disclosures", "raw_payload"}
)


def reject_sensitive_raw_fields(payload: Mapping[str, Any]) -> None:
    forbidden = SENSITIVE_RAW_FIELDS.intersection(payload)
    if forbidden:
        raise ValueError(
            "sensitive raw fields must not be persisted: "
            + ", ".join(sorted(forbidden))
        )


__all__ = ["SENSITIVE_RAW_FIELDS", "reject_sensitive_raw_fields"]
