from __future__ import annotations

from tigrbl_authz_resource_server_dpop_cnf_binding_validator import (
    DpopCnfBindingValidator,
)
from tigrbl_authz_resource_server_mtls_cnf_binding_validator import (
    MtlsCnfBindingValidator,
)
from tigrbl_identity_contracts.resource_server import AccessTokenClaims
from tigrbl_security_trust_contracts import DPoPBinding, MTLSBinding


class SenderConstraintValidator:
    """Compose resource-server DPoP and mTLS sender-constraint checks."""

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
            DpopCnfBindingValidator(self.dpop_confirmation_member).validate(claims, dpop)
        if require_mtls:
            MtlsCnfBindingValidator(self.mtls_confirmation_member).validate(claims, mtls)
        return True


__all__ = ["SenderConstraintValidator"]
