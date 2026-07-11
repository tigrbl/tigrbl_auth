"""Base classes for concrete OIDC strategies."""

from abc import ABC

from tigrbl_identity_contracts.oidc import (
    ClaimsProviderPort,
    ClaimsRequest,
    ClaimsResult,
    SubjectIdentifierRequest,
    SubjectIdentifierResult,
    SubjectIdentifierStrategyPort,
)


class ClaimsProviderBase(ClaimsProviderPort, ABC):
    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult:
        raise NotImplementedError


class SubjectIdentifierStrategyBase(SubjectIdentifierStrategyPort, ABC):
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        raise NotImplementedError


__all__ = ["ClaimsProviderBase", "SubjectIdentifierStrategyBase"]
