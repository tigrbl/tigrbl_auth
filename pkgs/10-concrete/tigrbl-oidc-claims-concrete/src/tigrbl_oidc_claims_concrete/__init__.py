from __future__ import annotations

from typing import Any, Mapping

from tigrbl_oidc_bases import ClaimsProviderBase
from tigrbl_identity_contracts.oidc import ClaimsRequest, ClaimsResult

from .eap import EapAcrValue, EapAmrValue, satisfies_eap_acr
from .identity_assurance import parse_verified_claims, serialize_verified_claims


class LocalClaimsProvider(ClaimsProviderBase):
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


__all__ = [
    "EapAcrValue",
    "EapAmrValue",
    "LocalClaimsProvider",
    "parse_verified_claims",
    "serialize_verified_claims",
    "satisfies_eap_acr",
]
