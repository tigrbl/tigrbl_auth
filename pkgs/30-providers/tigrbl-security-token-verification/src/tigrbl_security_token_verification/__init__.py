from __future__ import annotations

from typing import Any, Callable, Mapping

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_security_certificate_mtls import MtlsBindingValidator
from tigrbl_security_proof_dpop import DpopBindingValidator
from tigrbl_security_trust_contracts import (
    CapabilityMap,
    DPoPBinding,
    MTLSBinding,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
)
from tigrbl_security_trust_domain_bases import (
    ConfirmationBindingValidatorBase,
    JWKSCacheBase,
    SenderConstraintValidatorBase,
    TokenIntrospectionClientBase,
)


def _cnf_from(value: AccessTokenClaims | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(value, AccessTokenClaims):
        return value.cnf
    return value


class DpopCnfBindingValidator(ConfirmationBindingValidatorBase):
    """Validate DPoP confirmation material."""

    def __init__(
        self,
        confirmation_member: str = "jkt",
        *,
        provider: DpopBindingValidator | None = None,
    ) -> None:
        self.provider = provider or DpopBindingValidator()
        self.provider.confirmation_member = confirmation_member

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"confirmation-binding": ("dpop",)}, modes=("dpop",))

    @property
    def confirmation_member(self) -> str:
        return self.provider.confirmation_member

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: DPoPBinding | None,
    ) -> bool:
        return self.provider.validate_confirmation(cnf, binding)

    def validate(
        self,
        claims: AccessTokenClaims | Mapping[str, Any],
        binding: DPoPBinding | None,
    ) -> bool:
        if not self.validate_confirmation(_cnf_from(claims), binding):
            raise TokenValidationError("DPoP binding mismatch")
        return True


class MtlsCnfBindingValidator(ConfirmationBindingValidatorBase):
    """Validate mTLS confirmation material."""

    def __init__(
        self,
        confirmation_member: str = "x5t#S256",
        *,
        provider: MtlsBindingValidator | None = None,
    ) -> None:
        self.provider = provider or MtlsBindingValidator()
        self.provider.confirmation_member = confirmation_member

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"confirmation-binding": ("mtls",)}, modes=("mtls",))

    @property
    def confirmation_member(self) -> str:
        return self.provider.confirmation_member

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: MTLSBinding | None,
    ) -> bool:
        return self.provider.validate_confirmation(cnf, binding)

    def validate(
        self,
        claims: AccessTokenClaims | Mapping[str, Any],
        binding: MTLSBinding | None,
    ) -> bool:
        if not self.validate_confirmation(_cnf_from(claims), binding):
            raise TokenValidationError("mTLS binding mismatch")
        return True


class SenderConstraintValidator(SenderConstraintValidatorBase):
    """Compose DPoP and mTLS sender-constraint checks."""

    def __init__(
        self,
        dpop_confirmation_member: str = "jkt",
        mtls_confirmation_member: str = "x5t#S256",
    ) -> None:
        self.dpop_confirmation_member = dpop_confirmation_member
        self.mtls_confirmation_member = mtls_confirmation_member

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"sender-constraint": ("dpop", "mtls")},
            modes=("dpop", "mtls"),
        )

    def validate(
        self,
        claims: AccessTokenClaims | Mapping[str, Any],
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
        require_dpop: bool = False,
        require_mtls: bool = False,
    ) -> bool:
        cnf = _cnf_from(claims)
        if require_dpop:
            DpopCnfBindingValidator(self.dpop_confirmation_member).validate(cnf, dpop)
        if require_mtls:
            MtlsCnfBindingValidator(self.mtls_confirmation_member).validate(cnf, mtls)
        return True


class JWKSCache(JWKSCacheBase):
    """In-memory `kid` to JWK cache for protected-resource verification."""

    def __init__(self) -> None:
        self._keys: dict[str, Mapping[str, Any]] = {}

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"key-resolution": ("jwks",)}, formats=("jwk", "jwks"))

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        return dict(self._keys)

    def put_jwks(self, jwks: Mapping[str, Any]) -> None:
        for key in jwks.get("keys", []):
            kid = key.get("kid")
            if kid:
                self._keys[str(kid)] = dict(key)

    def get(self, kid: str) -> Mapping[str, Any]:
        try:
            return self._keys[kid]
        except KeyError as exc:
            raise TokenValidationError("unknown signing key") from exc


class IntrospectionClient(TokenIntrospectionClientBase):
    """Convert OAuth token introspection responses into access-token claims."""

    def __init__(
        self,
        transport: Callable[[str], Mapping[str, Any] | TokenIntrospectionResult],
    ) -> None:
        self.transport = transport

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"token-introspection": ("oauth2",)})

    def introspect_result(
        self,
        request: TokenIntrospectionRequest,
    ) -> TokenIntrospectionResult:
        payload = self.transport(request.token)
        if isinstance(payload, TokenIntrospectionResult):
            return payload
        return TokenIntrospectionResult(
            active=bool(payload.get("active")),
            claims=dict(payload),
        )

    def introspect(self, token: str | TokenIntrospectionRequest) -> AccessTokenClaims:
        request = token if isinstance(token, TokenIntrospectionRequest) else TokenIntrospectionRequest(token=token)
        result = self.introspect_result(request)
        if not result.active:
            raise TokenValidationError("introspection response is inactive")
        payload = dict(result.claims)
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


__all__ = [
    "DpopCnfBindingValidator",
    "IntrospectionClient",
    "JWKSCache",
    "MtlsCnfBindingValidator",
    "SenderConstraintValidator",
]
