"""Neutral attestation and reference-integrity contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence


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


class AttestationAppraiser(Protocol):
    def appraise(self, evidence: AttestationEvidence, /) -> AppraisalResult: ...


__all__ = ["AppraisalResult", "AttestationAppraiser", "AttestationEvidence", "ReferenceIntegrityManifest"]
