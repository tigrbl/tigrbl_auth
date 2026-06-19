from __future__ import annotations

"""Proof-binding validators for protected resource servers."""

from hmac import compare_digest

from .verifier import AccessTokenClaims, DPoPBinding, MTLSBinding, TokenValidationError


class MtlsBindingValidator:
    def __init__(self, confirmation_member: str = "x5t#S256") -> None:
        self.confirmation_member = confirmation_member

    def validate(self, claims: AccessTokenClaims, binding: MTLSBinding | None) -> bool:
        expected = str(claims.cnf.get(self.confirmation_member) or "").strip()
        presented = str(getattr(binding, "certificate_thumbprint", "") or "").strip()
        if binding is None or not expected or not compare_digest(presented, expected):
            raise TokenValidationError("mTLS binding mismatch")
        return True


class DpopValidator:
    def __init__(self, confirmation_member: str = "jkt") -> None:
        self.confirmation_member = confirmation_member

    def validate(self, claims: AccessTokenClaims, binding: DPoPBinding | None) -> bool:
        expected = str(claims.cnf.get(self.confirmation_member) or "").strip()
        presented = str(getattr(binding, "jwk_thumbprint", "") or "").strip()
        if binding is None or not expected or not compare_digest(presented, expected):
            raise TokenValidationError("DPoP binding mismatch")
        return True


class ProofBindingValidator:
    def __init__(
        self,
        dpop_confirmation_member: str = "jkt",
        mtls_confirmation_member: str = "x5t#S256",
    ) -> None:
        self.dpop_confirmation_member = dpop_confirmation_member
        self.mtls_confirmation_member = mtls_confirmation_member

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
            DpopValidator(self.dpop_confirmation_member).validate(claims, dpop)
        if require_mtls:
            MtlsBindingValidator(self.mtls_confirmation_member).validate(claims, mtls)
        return True


__all__ = ["DpopValidator", "MtlsBindingValidator", "ProofBindingValidator"]
