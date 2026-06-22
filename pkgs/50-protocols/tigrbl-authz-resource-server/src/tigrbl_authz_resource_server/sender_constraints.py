from __future__ import annotations

"""Sender-constraint validator facade for protected resource servers."""

from tigrbl_authz_resource_server_dpop_cnf_binding_validator import (
    DpopCnfBindingValidator,
)
from tigrbl_authz_resource_server_mtls_cnf_binding_validator import (
    MtlsCnfBindingValidator,
)

from .verifier import AccessTokenClaims, DPoPBinding, MTLSBinding


class SenderConstraintValidator:
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


__all__ = [
    "DpopCnfBindingValidator",
    "MtlsCnfBindingValidator",
    "SenderConstraintValidator",
]
