from __future__ import annotations

"""Proof-binding validators for protected resource servers."""

from dataclasses import dataclass

from .verifier import AccessTokenClaims, DPoPBinding, MTLSBinding, TokenValidationError


@dataclass(frozen=True, slots=True)
class MtlsBindingValidator:
    confirmation_member: str = "x5t#S256"

    def validate(self, claims: AccessTokenClaims, binding: MTLSBinding | None) -> bool:
        expected = claims.cnf.get(self.confirmation_member)
        if binding is None or not expected or binding.certificate_thumbprint != expected:
            raise TokenValidationError("mTLS binding mismatch")
        return True


@dataclass(frozen=True, slots=True)
class ProofBindingValidator:
    dpop_confirmation_member: str = "jkt"
    mtls_confirmation_member: str = "x5t#S256"

    def validate(
        self,
        claims: AccessTokenClaims,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
        require_dpop: bool = False,
        require_mtls: bool = False,
    ) -> bool:
        if require_dpop:
            expected = claims.cnf.get(self.dpop_confirmation_member)
            if dpop is None or not expected or dpop.jwk_thumbprint != expected:
                raise TokenValidationError("DPoP binding mismatch")
        if require_mtls:
            MtlsBindingValidator(self.mtls_confirmation_member).validate(claims, mtls)
        return True


__all__ = ["MtlsBindingValidator", "ProofBindingValidator"]
