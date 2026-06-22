from __future__ import annotations

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_security_certificate_mtls import MtlsBindingValidator
from tigrbl_security_trust_contracts import MTLSBinding


class MtlsCnfBindingValidator:
    """Validate resource-server mTLS `cnf` binding material."""

    def __init__(
        self,
        confirmation_member: str = "x5t#S256",
        *,
        provider: MtlsBindingValidator | None = None,
    ) -> None:
        self.provider = provider or MtlsBindingValidator()
        self.provider.confirmation_member = confirmation_member

    @property
    def confirmation_member(self) -> str:
        return self.provider.confirmation_member

    def validate(self, claims: AccessTokenClaims, binding: MTLSBinding | None) -> bool:
        if not self.provider.validate_confirmation(claims.cnf, binding):
            raise TokenValidationError("mTLS binding mismatch")
        return True


__all__ = ["MtlsCnfBindingValidator"]
