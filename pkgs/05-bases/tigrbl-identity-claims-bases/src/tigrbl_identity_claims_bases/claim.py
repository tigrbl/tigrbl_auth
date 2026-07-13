"""Base for one concrete, independently packaged claim object."""

from __future__ import annotations
from abc import ABC
from typing import Any, ClassVar
from tigrbl_identity_contracts.claims import Claim
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class ClaimBase(Claim, ABC):
    claim_name: ClassVar[str]
    default_claim_type: ClassVar[ClaimType]
    default_value_type: ClassVar[ClaimValueType]
    default_standards: ClassVar[tuple[str, ...]] = ()
    default_name_kind: ClassVar[ClaimNameKind] = ClaimNameKind.SPECIFICATION
    default_namespace: ClassVar[str | None] = None
    default_registry: ClassVar[str | None] = None

    def __init__(self, value: Any, *, required: bool = False):
        self.validate_value(value)
        super().__init__(
            self.claim_name,
            value,
            self.default_claim_type,
            self.default_value_type,
            self.default_standards,
            required,
            self.default_name_kind,
            self.default_namespace,
            self.default_registry,
        )

    @classmethod
    def validate_value(cls, value: Any) -> None:
        return None


__all__ = ["ClaimBase"]
