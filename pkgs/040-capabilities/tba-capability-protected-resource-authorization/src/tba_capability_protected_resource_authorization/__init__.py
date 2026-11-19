"""Composable protected-resource authorization capability."""

from __future__ import annotations

from tba_concrete_capability import Capability
from tba_contracts_identity.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tba_contracts_identity.resource_server import (
    AccessTokenClaims,
    ResourceRequirement,
    ResourceServerVerifierPort,
    VerificationResult,
)
from tba_contracts_security_trust import DPoPBinding, MTLSBinding

from .sender_constraints import SenderConstraintValidator


class ProtectedResourceAuthorizationCapability(Capability):
    """Delegate normalized protected-resource decisions to one verifier."""

    def __init__(self, verifier: ResourceServerVerifierPort | None) -> None:
        self._verifier = verifier
        super().__init__(
            CapabilityDefinition("protected-resource.authorization", "1.0"),
            operations={
                "verify_token": CapabilityOperation(
                    target=self.verify_token if verifier is not None else None,
                    delegated=True,
                ),
                "verify_claims": CapabilityOperation(
                    target=self.verify_claims if verifier is not None else None,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._verifier is not None,
                status="ready" if self._verifier is not None else "unbound",
            ),
        )

    def verify_token(
        self,
        token: str | AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
    ) -> VerificationResult:
        if self._verifier is None:  # construction rejects this path
            raise NotImplementedError("protected-resource verifier is not bound")
        result = self._verifier.verify_token(
            token,
            requirement,
            dpop=dpop,
            mtls=mtls,
        )
        return self._require_result(result)

    def verify_claims(
        self,
        claims: AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
    ) -> VerificationResult:
        if self._verifier is None:  # construction rejects this path
            raise NotImplementedError("protected-resource verifier is not bound")
        result = self._verifier.verify_claims(
            claims,
            requirement,
            dpop=dpop,
            mtls=mtls,
        )
        return self._require_result(result)

    @staticmethod
    def _require_result(result: object) -> VerificationResult:
        if not isinstance(result, VerificationResult):
            raise TypeError(
                "protected-resource verifier must return VerificationResult"
            )
        return result


__all__ = [
    "ProtectedResourceAuthorizationCapability",
    "SenderConstraintValidator",
]
