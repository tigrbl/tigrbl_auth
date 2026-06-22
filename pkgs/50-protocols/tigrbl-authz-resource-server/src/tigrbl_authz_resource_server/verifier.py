from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from tigrbl_authz_resource_server_jwks_cache import JWKSCache
from tigrbl_authz_resource_server_dpop_cnf_binding_validator import (
    DpopCnfBindingValidator,
)
from tigrbl_authz_resource_server_mtls_cnf_binding_validator import (
    MtlsCnfBindingValidator,
)
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


def _utc_timestamp() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


class IntrospectionClient:
    def __init__(self, transport: IntrospectionTransport) -> None:
        self.transport = transport

    def introspect(self, token: str) -> AccessTokenClaims:
        payload = dict(self.transport(token))
        if not payload.get("active"):
            raise TokenValidationError("introspection response is inactive")
        scope_value = payload.get("scope", ())
        scopes = tuple(scope_value.split()) if isinstance(scope_value, str) else tuple(scope_value)
        aud_value = payload.get("aud", ())
        audiences = (aud_value,) if isinstance(aud_value, str) else tuple(aud_value)
        return AccessTokenClaims(
            iss=str(payload["iss"]),
            sub=str(payload["sub"]),
            aud=audiences,
            exp=int(payload["exp"]),
            iat=int(payload.get("iat", 0)),
            scope=scopes,
            cnf=payload.get("cnf", {}),
        )


class ResourceServerVerifier:
    def __init__(
        self,
        *,
        jwks_cache: JWKSCache | None = None,
        introspection_client: IntrospectionClient | None = None,
        policy_hook: PolicyHook | None = None,
        now: Callable[[], int] = _utc_timestamp,
    ) -> None:
        self.jwks_cache = jwks_cache or JWKSCache()
        self.introspection_client = introspection_client
        self.policy_hook = policy_hook
        self.now = now

    def verify_claims(
        self,
        claims: AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
    ) -> VerificationResult:
        try:
            self._validate_token_claims(claims, requirement)
            self._validate_proof_bindings(claims, requirement, dpop=dpop, mtls=mtls)
            policy_reference = None
            if self.policy_hook is not None:
                allowed, policy_reference = self.policy_hook(claims, requirement)
                if not allowed:
                    return VerificationResult(
                        VerificationStatus.DENIED,
                        claims.sub,
                        "denied by policy hook",
                        policy_reference=policy_reference,
                    )
        except TokenValidationError as exc:
            return VerificationResult(
                VerificationStatus.DENIED,
                claims.sub if isinstance(claims, AccessTokenClaims) else None,
                str(exc),
            )
        return VerificationResult(
            VerificationStatus.ALLOWED,
            claims.sub,
            "allowed",
            matched_scopes=tuple(scope for scope in requirement.scopes if scope in claims.scope),
            policy_reference=policy_reference,
        )

    def verify_token(
        self,
        token: str | AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
    ) -> VerificationResult:
        if isinstance(token, AccessTokenClaims):
            return self.verify_claims(token, requirement, dpop=dpop, mtls=mtls)
        if self.introspection_client is None:
            return VerificationResult(
                VerificationStatus.DENIED,
                None,
                "opaque token requires introspection client",
            )
        return self.verify_claims(
            self.introspection_client.introspect(token),
            requirement,
            dpop=dpop,
            mtls=mtls,
        )

    def _validate_token_claims(self, claims: AccessTokenClaims, requirement: ResourceRequirement) -> None:
        if claims.iss != requirement.issuer:
            raise TokenValidationError("issuer mismatch")
        if requirement.audience not in claims.aud:
            raise TokenValidationError("audience mismatch")
        if claims.exp <= self.now():
            raise TokenValidationError("token expired")
        if requirement.max_authz_staleness_seconds is not None:
            authz_iat = int(getattr(claims, "iat", 0))
            if self.now() - authz_iat > requirement.max_authz_staleness_seconds:
                raise TokenValidationError("authorization snapshot stale")
        missing = set(requirement.scopes) - set(claims.scope)
        if missing:
            raise TokenValidationError(f"missing required scopes: {', '.join(sorted(missing))}")

    @staticmethod
    def _validate_proof_bindings(
        claims: AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None,
        mtls: MTLSBinding | None,
    ) -> None:
        if requirement.require_dpop:
            DpopCnfBindingValidator().validate(claims, dpop)
        if requirement.require_mtls:
            MtlsCnfBindingValidator().validate(claims, mtls)


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
