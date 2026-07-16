from __future__ import annotations

from typing import Any, Mapping

from tigrbl_dpop_confirmation_binding_concrete import DpopCnfBindingValidator
from tigrbl_identity_contracts.resource_server import AccessTokenClaims
from tigrbl_mtls_confirmation_binding_concrete import MtlsCnfBindingValidator
from tigrbl_security_trust_contracts import CapabilityMap, DPoPBinding, MTLSBinding


def _cnf_from(value: AccessTokenClaims | Mapping[str, Any]) -> Mapping[str, Any]:
    return value.cnf if isinstance(value, AccessTokenClaims) else value


class SenderConstraintValidator:
    """Compose DPoP and mTLS confirmation-binding implementations."""

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
