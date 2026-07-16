"""Concrete `sub_ids` subject-information field."""

from collections.abc import Mapping, Sequence

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class SubjectIdentifiersClaim(ClaimBase):
    claim_name = "sub_ids"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.JSON_VALUE
    default_standards = ("RFC 9635",)

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, Sequence)
            or isinstance(value, (str, bytes))
            or not value
            or any(
                not isinstance(item, Mapping)
                or not isinstance(item.get("format"), str)
                or not isinstance(item.get("id"), str)
                for item in value
            )
        ):
            raise ValueError("sub_ids must contain subject identifier objects")


__all__ = ["SubjectIdentifiersClaim"]
