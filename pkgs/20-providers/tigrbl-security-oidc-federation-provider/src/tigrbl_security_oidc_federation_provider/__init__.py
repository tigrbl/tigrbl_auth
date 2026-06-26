from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.oidc import FederationEntityStatementRequest, FederationEntityStatementResult
from tigrbl_security_trust_contracts import CapabilityMap
from tigrbl_security_trust_domain_bases import OidcFederationProviderBase


class StaticOidcFederationProvider(OidcFederationProviderBase):
    def __init__(self, statements: Mapping[str, str | Mapping[str, Any]] | None = None) -> None:
        self._statements = dict(statements or {})

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"entity_statement": ("static",)}, features=("oidc-federation",))

    async def entity_statement(
        self,
        request: FederationEntityStatementRequest,
    ) -> FederationEntityStatementResult:
        statement = self._statements.get(request.entity_id, {"sub": request.entity_id})
        return FederationEntityStatementResult(request.entity_id, statement)


__all__ = ["StaticOidcFederationProvider"]
