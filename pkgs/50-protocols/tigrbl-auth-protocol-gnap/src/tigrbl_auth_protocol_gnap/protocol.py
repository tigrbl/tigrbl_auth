"""RFC 9635 mapping to the neutral grant-negotiation capability."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from tigrbl_grant_negotiation_capability import GrantNegotiationCapability
from tigrbl_identity_contracts.gnap import GrantContinuationRequest

from .schemas import GnapRequest, parse_gnap_request, serialize_gnap_result


class GnapProtocol:
    version = "RFC9635"

    def __init__(self, capability: GrantNegotiationCapability):
        self._capability = capability

    async def grant(self, payload: Mapping[str, Any]) -> dict[str, object]:
        request = parse_gnap_request(payload).to_contract()
        return serialize_gnap_result(await self._capability.request(request))

    async def continue_grant(
        self,
        continuation_token: str,
        *,
        proof: str | bytes | Mapping[str, object] | None = None,
    ) -> dict[str, object]:
        request = GrantContinuationRequest(continuation_token, proof)
        return serialize_gnap_result(await self._capability.continue_request(request))

    async def rotate_access_token(
        self,
        management_token: str,
        *,
        proof: str | bytes | Mapping[str, object] | None = None,
    ) -> dict[str, object]:
        request = GrantContinuationRequest(management_token, proof)
        return serialize_gnap_result(await self._capability.rotate(request))


__all__ = ["GnapProtocol", "GnapRequest", "parse_gnap_request"]
