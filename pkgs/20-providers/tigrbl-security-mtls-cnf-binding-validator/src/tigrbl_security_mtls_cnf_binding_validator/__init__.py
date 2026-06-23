from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_security_certificate_mtls import MtlsBindingValidator
from tigrbl_security_trust_contracts import CapabilityMap, MTLSBinding
from tigrbl_security_trust_domain_bases import ConfirmationBindingValidatorBase


def _cnf_from(value: AccessTokenClaims | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(value, AccessTokenClaims):
        return value.cnf
    return value


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


__all__ = ["MtlsCnfBindingValidator"]
