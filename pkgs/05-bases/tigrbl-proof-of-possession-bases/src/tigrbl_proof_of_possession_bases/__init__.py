"""Reusable proof-of-possession bases."""

from abc import ABC, abstractmethod
from typing import Any, Mapping

from tigrbl_protected_artifact_bases import ProtectedArtifactVerifierBase, SecurityArtifactIssuerBase
from tigrbl_security_trust_contracts import (
    DPoPBinding,
    ICapabilityProvider,
    IConfirmationBindingValidator,
    IPkceVerifier,
    ISenderConstraintValidator,
    MTLSBinding,
    ProofBinding,
)


class ProofOfPossessionDomainBase(
    ICapabilityProvider,
    SecurityArtifactIssuerBase,
    ProtectedArtifactVerifierBase,
    ABC,
):
    """Artifact-oriented proof-of-possession composition."""


class PkceVerifierBase(IPkceVerifier, ICapabilityProvider, ABC):
    def verify_challenge(self, *, verifier: str, challenge: str) -> bool:
        raise NotImplementedError


class ConfirmationBindingValidatorBase(IConfirmationBindingValidator, ICapabilityProvider, ABC):
    @property
    @abstractmethod
    def confirmation_member(self) -> str: ...

    def validate_confirmation(self, cnf: Mapping[str, Any], binding: ProofBinding | None) -> bool:
        raise NotImplementedError


class SenderConstraintValidatorBase(ISenderConstraintValidator, ICapabilityProvider, ABC):
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
    "PkceVerifierBase",
    "ProofOfPossessionDomainBase",
    "SenderConstraintValidatorBase",
]
