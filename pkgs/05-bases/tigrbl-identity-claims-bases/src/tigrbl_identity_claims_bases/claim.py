"""Base for one concrete, independently packaged claim object."""

from __future__ import annotations
from abc import ABC
from typing import Any, ClassVar
from tigrbl_identity_contracts.claims import Claim
from tigrbl_identity_core import ClaimType, ClaimValueType


class ClaimBase(Claim, ABC):
    claim_name: ClassVar[str]
    default_claim_type: ClassVar[ClaimType]
    default_value_type: ClassVar[ClaimValueType]
    default_standards: ClassVar[tuple[str, ...]] = ()

    def __init__(self, value: Any, *, required: bool = False):
        self.validate_value(value)
        super().__init__(
            self.claim_name,
            value,
            self.default_claim_type,
            self.default_value_type,
            self.default_standards,
            required,
        )

    @classmethod
    def validate_value(cls, value: Any) -> None:
        return None


__all__ = ["ClaimBase"]
