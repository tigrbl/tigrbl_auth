"""Possession-proof extension ports."""

from typing import Protocol

from .proofs import PossessionProof, PossessionProofContext
from .verification import PossessionProofVerificationRequest, PossessionProofVerificationResult


class PossessionProofIssuerPort(Protocol):
    def issue(self, context: PossessionProofContext, /) -> PossessionProof: ...


class PossessionProofVerifierPort(Protocol):
    def verify(self, request: PossessionProofVerificationRequest, /) -> PossessionProofVerificationResult: ...


class ConfirmationKeyResolverPort(Protocol):
    def resolve_confirmation_key(self, confirmation: object, /) -> object: ...


class ProofContextBindingEvaluatorPort(Protocol):
    def evaluate_context(self, expected: PossessionProofContext, presented: PossessionProofContext, /) -> bool: ...


__all__ = ["ConfirmationKeyResolverPort", "PossessionProofIssuerPort", "PossessionProofVerifierPort", "ProofContextBindingEvaluatorPort"]