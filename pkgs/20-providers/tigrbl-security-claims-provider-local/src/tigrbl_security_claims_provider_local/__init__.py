from __future__ import annotations

from tigrbl_identity_contracts.oidc import ClaimsRequest, ClaimsResult
from tigrbl_oidc_claims_concrete import LocalClaimsProvider
from tigrbl_security_trust_contracts import CapabilityMap
from tigrbl_security_trust_domain_bases import ClaimsProviderBase


class LocalSecurityClaimsProvider(ClaimsProviderBase):
    def __init__(self, provider: LocalClaimsProvider | None = None) -> None:
        self._provider = provider or LocalClaimsProvider()

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"claims": ("local",)}, features=("oidc-claims",))

    async def claims(self, request: ClaimsRequest) -> ClaimsResult:
        return await self._provider.claims(request)


__all__ = ["LocalSecurityClaimsProvider"]
