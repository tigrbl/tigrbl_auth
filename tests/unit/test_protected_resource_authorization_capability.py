from __future__ import annotations

import pytest

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    ResourceRequirement,
    VerificationResult,
    VerificationStatus,
)
from tigrbl_protected_resource_authorization_capability import (
    ProtectedResourceAuthorizationCapability,
)


class _Verifier:
    def verify_token(self, token, requirement, *, dpop=None, mtls=None):
        return VerificationResult(
            VerificationStatus.ALLOWED,
            "subject-1",
            "token allowed",
            matched_scopes=requirement.scopes,
        )

    def verify_claims(self, claims, requirement, *, dpop=None, mtls=None):
        return VerificationResult(
            VerificationStatus.ALLOWED,
            claims.sub,
            "claims allowed",
            matched_scopes=requirement.scopes,
        )


def _requirement() -> ResourceRequirement:
    return ResourceRequirement(
        issuer="https://issuer.example",
        audience="api://resource",
        scopes=("read",),
    )


def _claims() -> AccessTokenClaims:
    return AccessTokenClaims(
        iss="https://issuer.example",
        sub="subject-1",
        aud=("api://resource",),
        exp=2_000_000_000,
        iat=1_999_999_900,
        scope=("read",),
    )


def test_protected_resource_capability_requires_a_verifier() -> None:
    with pytest.raises(NotImplementedError, match="verify_claims|verify_token"):
        ProtectedResourceAuthorizationCapability(None)


@pytest.mark.asyncio
async def test_protected_resource_capability_delegates_both_operations() -> None:
    capability = ProtectedResourceAuthorizationCapability(_Verifier())

    token_call = await capability.call("verify_token", "opaque", _requirement())
    claims_call = await capability.call("verify_claims", _claims(), _requirement())

    assert token_call.value.reason == "token allowed"
    assert claims_call.value.reason == "claims allowed"
    assert token_call.delegated and claims_call.delegated
    assert capability.capability_report()["operations"] == (
        "verify_token",
        "verify_claims",
    )
    assert capability.state().ready is True


def test_protected_resource_capability_rejects_untyped_results() -> None:
    class _InvalidVerifier(_Verifier):
        def verify_token(self, token, requirement, *, dpop=None, mtls=None):
            return object()

    capability = ProtectedResourceAuthorizationCapability(_InvalidVerifier())
    with pytest.raises(TypeError, match="must return VerificationResult"):
        capability.verify_token("opaque", _requirement())
