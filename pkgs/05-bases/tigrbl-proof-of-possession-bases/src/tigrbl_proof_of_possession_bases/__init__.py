"""Reusable proof-of-possession bases."""

from abc import ABC, abstractmethod
from typing import Any, Mapping

from tigrbl_proof_of_possession_contracts import (
    ConfirmationKeyResolverPort,
    PossessionProof,
    PossessionProofContext,
    PossessionProofIssuerPort,
    PossessionProofVerificationRequest,
    PossessionProofVerificationResult,
    PossessionProofVerifierPort,
    ProofContextBindingEvaluatorPort,
)
from tigrbl_protected_artifact_bases import (
    ProtectedArtifactVerifierBase,
    SecurityArtifactIssuerBase,
)
from tigrbl_security_trust_contracts import (
    DPoPBinding,
    ICapabilityProvider,
    IConfirmationBindingValidator,
    IPkceVerifier,
    ISenderConstraintValidator,
    MTLSBinding,
    ProofBinding,
)


class PossessionProofIssuerBase(PossessionProofIssuerPort, ABC):
    def issue(self, context: PossessionProofContext, /) -> PossessionProof:
        raise NotImplementedError


class PossessionProofVerifierBase(PossessionProofVerifierPort, ABC):
    def verify(
        self,
        request: PossessionProofVerificationRequest,
        /,
    ) -> PossessionProofVerificationResult:
        raise NotImplementedError


class ConfirmationKeyResolverBase(ConfirmationKeyResolverPort, ABC):
    def resolve_confirmation_key(self, confirmation: object, /) -> object:
        raise NotImplementedError


class ProofContextBindingEvaluatorBase(ProofContextBindingEvaluatorPort, ABC):
    def evaluate_context(
        self,
        expected: PossessionProofContext,
        presented: PossessionProofContext,
        /,
    ) -> bool:
        raise NotImplementedError


# Compatibility bases retained until legacy DPoP/mTLS consumers migrate to the
# carrier-neutral proof contracts above.
class ProofOfPossessionDomainBase(
    ICapabilityProvider,
    SecurityArtifactIssuerBase,
    ProtectedArtifactVerifierBase,
    ABC,
):
    """Legacy artifact-oriented proof composition."""


class PkceVerifierBase(IPkceVerifier, ICapabilityProvider, ABC):
    def verify_challenge(self, *, verifier: str, challenge: str) -> bool:
        raise NotImplementedError


class ConfirmationBindingValidatorBase(
    IConfirmationBindingValidator,
    ICapabilityProvider,
    ABC,
):
    @property
    @abstractmethod
    def confirmation_member(self) -> str: ...

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: ProofBinding | None,
    ) -> bool:
        raise NotImplementedError


class SenderConstraintValidatorBase(
    ISenderConstraintValidator,
    ICapabilityProvider,
    ABC,
):
    def validate(
        self,
        cnf: Mapping[str, Any],
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
        require_dpop: bool = False,
        require_mtls: bool = False,
    ) -> bool:
        raise NotImplementedError


__all__ = [
    "ConfirmationBindingValidatorBase",
    "ConfirmationKeyResolverBase",
    "PkceVerifierBase",
    "PossessionProofIssuerBase",
    "PossessionProofVerifierBase",
    "ProofContextBindingEvaluatorBase",
    "ProofOfPossessionDomainBase",
    "SenderConstraintValidatorBase",
]