"""Protocol-neutral bases for claims production and assurance validation."""

from abc import ABC
from tigrbl_identity_contracts.claims import (
    ClaimsProviderPort,
    ClaimsRequest,
    ClaimsResult,
)


class ClaimsProviderBase(ClaimsProviderPort, ABC):
    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult:
        raise NotImplementedError


__all__ = ["ClaimsProviderBase"]
