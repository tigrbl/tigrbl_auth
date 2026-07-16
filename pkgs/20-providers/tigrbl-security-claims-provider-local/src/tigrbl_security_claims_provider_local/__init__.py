from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.claims import ClaimsRequest, ClaimsResult
from tigrbl_claim_bases import ClaimsProviderBase
from tigrbl_security_trust_contracts import CapabilityMap


class LocalClaimsProvider(ClaimsProviderBase):
    """Resolve claims from caller-supplied local identity records.

    This is environment-backed behavior and therefore belongs to layer 20.
    It deliberately emits ordinary claims only; verified claims require an
    assurance provider with evidence and framework metadata.
    """

    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult:
        source: Mapping[str, Any] = {}
        if request.user is not None:
            source = dict(getattr(request.user, "model_dump", lambda: {})())
        claims: dict[str, Any] = {"sub": request.subject}
        for descriptor in request.requested_claims:
            if descriptor.name in source:
                claims[descriptor.name] = source[descriptor.name]
        if "profile" in request.scopes:
            for field in ("name", "given_name", "family_name", "preferred_username"):
                if field in source:
                    claims.setdefault(field, source[field])
        if "email" in request.scopes and "email" in source:
            claims.setdefault("email", source["email"])
        return ClaimsResult(claims=claims)


class LocalSecurityClaimsProvider(LocalClaimsProvider):
    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"claims": ("local",)}, features=("oidc-claims",))


__all__ = ["LocalClaimsProvider", "LocalSecurityClaimsProvider"]
