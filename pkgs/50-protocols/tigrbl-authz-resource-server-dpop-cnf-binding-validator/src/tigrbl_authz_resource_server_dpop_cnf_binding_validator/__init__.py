from __future__ import annotations

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_security_proof_dpop import DpopBindingValidator
from tigrbl_security_trust_contracts import DPoPBinding


class DpopCnfBindingValidator:
    """Validate resource-server DPoP `cnf` binding material."""

    def __init__(
        self,
        confirmation_member: str = "jkt",
        *,
        provider: DpopBindingValidator | None = None,
    ) -> None:
        self.provider = provider or DpopBindingValidator()
        self.provider.confirmation_member = confirmation_member

    @property
    def confirmation_member(self) -> str:
        return self.provider.confirmation_member

    def validate(self, claims: AccessTokenClaims, binding: DPoPBinding | None) -> bool:
        if not self.provider.validate_confirmation(claims.cnf, binding):
            raise TokenValidationError("DPoP binding mismatch")
        return True


__all__ = ["DpopCnfBindingValidator"]
