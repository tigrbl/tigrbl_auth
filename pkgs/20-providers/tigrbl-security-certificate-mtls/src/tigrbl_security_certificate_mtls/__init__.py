from __future__ import annotations

from hmac import compare_digest
from typing import Any, Mapping

from tigrbl_security_trust_contracts import (
    CapabilityMap,
    CertificateVerifyRequest,
    MTLSBinding,
    VerificationResult,
    VerifyRequest,
)
from tigrbl_certificate_bases import CertificateServiceDomainBase


class MtlsBindingValidator(CertificateServiceDomainBase):
    """Validate mTLS certificate confirmation-claim binding material."""

    confirmation_member = "x5t#S256"

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"verify": ("mtls",)},
            modes=("mtls",),
            features=("cnf-binding", "certificate-binding"),
        )

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: MTLSBinding | None,
    ) -> bool:
        expected = str(cnf.get(self.confirmation_member) or "").strip()
        presented = str(getattr(binding, "certificate_thumbprint", "") or "").strip()
        return binding is not None and bool(expected) and compare_digest(presented, expected)

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        binding = request.context.get("binding")
        cnf = request.context.get("cnf", {})
        if not isinstance(cnf, Mapping):
            return VerificationResult(valid=False, reason="mTLS cnf context must be a mapping")
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


__all__ = ["MtlsBindingValidator"]
