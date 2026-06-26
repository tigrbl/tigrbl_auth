from __future__ import annotations

from tigrbl_identity_contracts.oidc import WebFingerRequest, WebFingerResult
from tigrbl_security_trust_contracts import CapabilityMap
from tigrbl_security_trust_domain_bases import WebFingerResolverBase


class WebFingerProvider(WebFingerResolverBase):
    def __init__(self, issuer: str) -> None:
        self.issuer = issuer

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"webfinger": ("static",)}, features=("webfinger", "oidc-discovery"))

    async def resolve(self, request: WebFingerRequest) -> WebFingerResult:
        return WebFingerResult(
            subject=request.resource,
            links=({"rel": request.rel, "href": self.issuer},),
        )


__all__ = ["WebFingerProvider"]
