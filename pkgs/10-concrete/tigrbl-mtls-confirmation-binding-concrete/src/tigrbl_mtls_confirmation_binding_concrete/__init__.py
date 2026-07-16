from __future__ import annotations

from hmac import compare_digest
from typing import Any, Mapping

from tigrbl_certificate_bases import CertificateServiceDomainBase
from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_proof_of_possession_bases import ConfirmationBindingValidatorBase
from tigrbl_security_trust_contracts import (
    CapabilityMap,
    CertificateVerifyRequest,
    MTLSBinding,
    VerificationResult,
    VerifyRequest,
)


def _cnf_from(value: AccessTokenClaims | Mapping[str, Any]) -> Mapping[str, Any]:
    return value.cnf if isinstance(value, AccessTokenClaims) else value


class MtlsBindingValidator(CertificateServiceDomainBase):
    """Compare a certificate thumbprint with the corresponding cnf member."""

    confirmation_member = "x5t#S256"

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"verify": ("mtls",)},
            modes=("mtls",),
            features=("cnf-binding", "certificate-binding"),
        )

    def validate_confirmation(
        self, cnf: Mapping[str, Any], binding: MTLSBinding | None
    ) -> bool:
        expected = str(cnf.get(self.confirmation_member) or "").strip()
        presented = str(getattr(binding, "certificate_thumbprint", "") or "").strip()
        return (
            binding is not None
            and bool(expected)
            and compare_digest(presented, expected)
        )

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        binding = request.context.get("binding")
        cnf = request.context.get("cnf", {})
        if not isinstance(cnf, Mapping):
            return VerificationResult(
                valid=False, reason="mTLS cnf context must be a mapping"
            )
        if not isinstance(binding, MTLSBinding):
            return VerificationResult(valid=False, reason="missing mTLS binding")
        valid = self.validate_confirmation(cnf, binding)
        return VerificationResult(
            valid=valid,
            reason=None if valid else "mTLS binding mismatch",
            claims=binding.confirmation_claim,
            meta={"method": "mtls"},
        )

    async def verify_certificate(
        self, request: CertificateVerifyRequest
    ) -> VerificationResult:
        return VerificationResult(
            valid=True,
            reason=None,
            meta={"check_revocation": request.check_revocation},
        )


class MtlsCnfBindingValidator(ConfirmationBindingValidatorBase):
    """Validate mTLS confirmation material on access-token claims."""

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
        self, cnf: Mapping[str, Any], binding: MTLSBinding | None
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


__all__ = ["MtlsBindingValidator", "MtlsCnfBindingValidator"]
