from __future__ import annotations

from hmac import compare_digest
from typing import Any, Mapping

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_proof_of_possession_bases import (
    ConfirmationBindingValidatorBase,
    ProofOfPossessionDomainBase,
)
from tigrbl_security_trust_contracts import (
    CapabilityMap,
    DPoPBinding,
    VerificationResult,
    VerifyRequest,
)


def _cnf_from(value: AccessTokenClaims | Mapping[str, Any]) -> Mapping[str, Any]:
    return value.cnf if isinstance(value, AccessTokenClaims) else value


class DpopBindingValidator(ProofOfPossessionDomainBase):
    """Compare a DPoP JWK thumbprint with the corresponding cnf member."""

    confirmation_member = "jkt"

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"verify": ("dpop",)},
            modes=("dpop",),
            features=("cnf-binding", "proof-of-possession"),
        )

    def validate_confirmation(
        self, cnf: Mapping[str, Any], binding: DPoPBinding | None
    ) -> bool:
        expected = str(cnf.get(self.confirmation_member) or "").strip()
        presented = str(getattr(binding, "jwk_thumbprint", "") or "").strip()
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
                valid=False, reason="DPoP cnf context must be a mapping"
            )
        if not isinstance(binding, DPoPBinding):
            return VerificationResult(valid=False, reason="missing DPoP binding")
        valid = self.validate_confirmation(cnf, binding)
        return VerificationResult(
            valid=valid,
            reason=None if valid else "DPoP binding mismatch",
            claims=binding.confirmation_claim,
            meta={"method": "dpop"},
        )


class DpopCnfBindingValidator(ConfirmationBindingValidatorBase):
    """Validate DPoP confirmation material on access-token claims."""

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
        self, cnf: Mapping[str, Any], binding: DPoPBinding | None
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


__all__ = ["DpopBindingValidator", "DpopCnfBindingValidator"]
