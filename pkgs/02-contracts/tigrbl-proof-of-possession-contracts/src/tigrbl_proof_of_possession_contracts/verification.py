"""Possession-proof verification requests and results."""

from dataclasses import dataclass, field
from typing import Mapping

from .confirmation import ConfirmationKeyBinding
from .proofs import PossessionProof, PossessionProofContext


@dataclass(frozen=True, slots=True)
class PossessionProofVerificationRequest:
    proof: PossessionProof
    confirmation: ConfirmationKeyBinding
    context: PossessionProofContext


@dataclass(frozen=True, slots=True)
class PossessionProofVerificationResult:
    valid: bool
    subject: str | None = None
    proof_id: str | None = None
    replay_accepted: bool | None = None
    reason: str | None = None
    evidence: Mapping[str, object] = field(default_factory=dict)


__all__ = ["PossessionProofVerificationRequest", "PossessionProofVerificationResult"]