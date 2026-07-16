"""Protocol-neutral bases for claims production and assurance validation."""

from abc import ABC
from tigrbl_claim_contracts import (
    ClaimsProviderPort,
    ClaimsRequest,
    ClaimsResult,
)
from .claim import ClaimBase
from .claim_set import ClaimSetComposerBase


class ClaimsProviderBase(ClaimsProviderPort, ABC):
    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult:
        raise NotImplementedError


__all__ = ["ClaimBase", "ClaimSetComposerBase", "ClaimsProviderBase"]
