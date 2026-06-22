from __future__ import annotations

from tigrbl_authz_resource_server_verifier import ResourceServerVerifier

from tigrbl_authz_resource_server_introspection_client import IntrospectionClient
from tigrbl_authz_resource_server_jwks_cache import JWKSCache
from tigrbl_security_trust_contracts import DPoPBinding, MTLSBinding
from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    FrameworkRequest,
    IntrospectionTransport,
    PolicyHook,
    ResourceRequirement,
    ResourceServerError,
    TokenValidationError,
    VerificationResult,
    VerificationStatus,
)


def bearer_token_from_authorization(value: str | None) -> str | None:
    if not value:
        return None
    scheme, _, token = value.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token


def verify_framework_request(
    verifier: ResourceServerVerifier,
    request: FrameworkRequest,
    requirement: ResourceRequirement,
) -> VerificationResult:
    token = bearer_token_from_authorization(request.authorization)
    if token is None:
        return VerificationResult(VerificationStatus.DENIED, None, "missing bearer token")
    return verifier.verify_token(token, requirement, dpop=request.dpop, mtls=request.mtls)


__all__ = [
    "AccessTokenClaims",
    "DPoPBinding",
    "FrameworkRequest",
    "IntrospectionClient",
    "IntrospectionTransport",
    "JWKSCache",
    "MTLSBinding",
    "PolicyHook",
    "ResourceRequirement",
    "ResourceServerError",
    "ResourceServerVerifier",
    "TokenValidationError",
    "VerificationResult",
    "VerificationStatus",
    "bearer_token_from_authorization",
    "verify_framework_request",
]
