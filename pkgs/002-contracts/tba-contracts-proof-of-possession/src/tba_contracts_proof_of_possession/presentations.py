"""Credential presentations carrying explicit possession proof."""

from dataclasses import dataclass

from .proofs import PossessionProofContext


@dataclass(frozen=True, slots=True)
class CredentialPossessionPresentation:
    credential: bytes | str
    proof: bytes | str
    context: PossessionProofContext
    credential_profile: str
    proof_profile: str


__all__ = ["CredentialPossessionPresentation"]