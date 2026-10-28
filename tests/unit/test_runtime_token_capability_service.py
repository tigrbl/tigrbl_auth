from __future__ import annotations

from pathlib import Path

import pytest

from tba_contracts_identity.capabilities import CapabilityDefinition
from tba_contracts_identity.tokens import (
    IssuedTokenPair,
    RefreshTokenRedemptionRequest,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
    TokenPairIssueRequest,
    TokenRevocationRequest,
    TokenRevocationResult,
)
from tba_runtime_identity import CapabilityFactory, CapabilityRegistry
from tba_runtime_identity.token_service import RuntimeTokenService
from tba_capability_token_introspection import TokenIntrospectionCapability
from tba_capability_token_issuance import TokenIssuanceCapability
from tba_capability_token_revocation import TokenRevocationCapability


def _registry() -> CapabilityRegistry:
    async def issue(request: TokenPairIssueRequest) -> IssuedTokenPair:
        return IssuedTokenPair("access", "refresh")

    async def redeem(request: RefreshTokenRedemptionRequest) -> IssuedTokenPair:
        return IssuedTokenPair("next-access", "next-refresh")

    async def introspect(token: str) -> TokenIntrospectionResult:
        return TokenIntrospectionResult(True, {"sub": "subject"})

    async def revoke(token: str, token_type: str | None, reason: str):
        return TokenRevocationResult(True, token)

    return CapabilityRegistry(
        (
            TokenIntrospectionCapability(introspect),
            TokenRevocationCapability(revoke),
        ),
        factories=(
            CapabilityFactory(
                CapabilityDefinition("token.issuance", "1.0"),
                ("issue_token_pair", "redeem_refresh_token"),
                lambda db: TokenIssuanceCapability(issue, redeem),
            ),
        ),
    )


@pytest.mark.asyncio
async def test_runtime_token_service_dispatches_typed_capability_operations() -> None:
    service = RuntimeTokenService(_registry(), db=object())

    issued = await service.issue_token_pair(
        TokenPairIssueRequest("subject", "tenant", "client", "issuer")
    )
    redeemed = await service.redeem_refresh_token(
        RefreshTokenRedemptionRequest("refresh", "tenant", "client")
    )
    introspected = await service.introspect_token(TokenIntrospectionRequest("access"))
    revoked = await service.revoke_token(TokenRevocationRequest("access"))

    assert issued.access_token == "access"
    assert redeemed.access_token == "next-access"
    assert introspected.active
    assert revoked.token_reference == "access"


def test_runtime_token_service_keeps_storage_imports_in_compatibility_module() -> None:
    package_root = (
        Path("pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity")
    )
    canonical = (package_root / "token_service.py").read_text(encoding="utf-8")
    compatibility = (package_root / "token_service_compat.py").read_text(
        encoding="utf-8"
    )

    assert "tba_runtime_identity_storage" not in canonical
    assert "tba_runtime_identity_storage" in compatibility
