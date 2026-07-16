from __future__ import annotations

from hmac import compare_digest
from typing import Any, Mapping

from tigrbl_security_trust_contracts import (
    CapabilityMap,
    DPoPBinding,
    VerificationResult,
    VerifyRequest,
)
from tigrbl_proof_of_possession_bases import ProofOfPossessionDomainBase


class DpopBindingValidator(ProofOfPossessionDomainBase):
    """Validate DPoP confirmation-claim binding material."""

    confirmation_member = "jkt"

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"verify": ("dpop",)},
            modes=("dpop",),
            features=("cnf-binding", "proof-of-possession"),
        )

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: DPoPBinding | None,
    ) -> bool:
        expected = str(cnf.get(self.confirmation_member) or "").strip()
        presented = str(getattr(binding, "jwk_thumbprint", "") or "").strip()
        return binding is not None and bool(expected) and compare_digest(presented, expected)

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        binding = request.context.get("binding")
        cnf = request.context.get("cnf", {})
        if not isinstance(cnf, Mapping):
            return VerificationResult(valid=False, reason="DPoP cnf context must be a mapping")
        if not isinstance(binding, DPoPBinding):
            return VerificationResult(valid=False, reason="missing DPoP binding")
        valid = self.validate_confirmation(cnf, binding)
        return VerificationResult(
            valid=valid,
            reason=None if valid else "DPoP binding mismatch",
            claims=binding.confirmation_claim,
            meta={"method": "dpop"},
        )


__all__ = ["DpopBindingValidator"]
