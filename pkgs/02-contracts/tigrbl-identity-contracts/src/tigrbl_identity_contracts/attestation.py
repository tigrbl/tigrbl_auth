"""Neutral attestation and reference-integrity contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence

from .tokens import VerifiedTokenEnvelope


@dataclass(frozen=True, slots=True)
class AttestationEvidence:
    profile: str
    claims: Mapping[str | int, Any]
    raw: bytes | str | None = None


@dataclass(frozen=True, slots=True)
class ReferenceIntegrityManifest:
    tag_identity: str
    manifests: Sequence[Mapping[str, Any]]
    signer: str | None = None


@dataclass(frozen=True, slots=True)
class AppraisalResult:
    trusted: bool
    reason: str
    claims: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class VerifiedAttestationEvidence:
    """Evidence whose protected envelope and profile binding were verified."""

    evidence: AttestationEvidence
    envelope: VerifiedTokenEnvelope


@dataclass(frozen=True, slots=True)
class EvidenceVerificationResult:
    """Integrity result, deliberately distinct from a trust appraisal."""

    verified: bool
    reason: str
    evidence: VerifiedAttestationEvidence | None = None
    claims: Mapping[str | int, Any] = field(default_factory=dict)

    @property
    def trusted(self) -> bool:
        """Compatibility view; verification alone is not an appraisal."""

        return self.verified


class AttestationAppraiser(Protocol):
    def appraise(
        self, evidence: VerifiedAttestationEvidence, /
    ) -> AppraisalResult: ...


class EvidenceVerifierPort(Protocol):
    def verify_evidence(
        self, evidence: AttestationEvidence, /
    ) -> EvidenceVerificationResult: ...


class AttestationAppraiserPort(Protocol):
    def appraise(
        self, evidence: VerifiedAttestationEvidence, /
    ) -> AppraisalResult: ...


class ReferenceMaterialProviderPort(Protocol):
    def resolve_manifest(self, tag_identity: str, /) -> ReferenceIntegrityManifest: ...


__all__ = [
    "AppraisalResult",
    "AttestationAppraiser",
    "AttestationAppraiserPort",
    "AttestationEvidence",
    "EvidenceVerifierPort",
    "EvidenceVerificationResult",
    "ReferenceIntegrityManifest",
    "ReferenceMaterialProviderPort",
    "VerifiedAttestationEvidence",
]
