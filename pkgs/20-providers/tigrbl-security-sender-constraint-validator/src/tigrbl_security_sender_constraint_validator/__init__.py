from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.resource_server import AccessTokenClaims
from tigrbl_security_dpop_cnf_binding_validator import DpopCnfBindingValidator
from tigrbl_security_mtls_cnf_binding_validator import MtlsCnfBindingValidator
from tigrbl_security_trust_contracts import CapabilityMap, DPoPBinding, MTLSBinding
from tigrbl_proof_of_possession_bases import SenderConstraintValidatorBase


def _cnf_from(value: AccessTokenClaims | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(value, AccessTokenClaims):
        return value.cnf
    return value


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


__all__ = ["SenderConstraintValidator"]
