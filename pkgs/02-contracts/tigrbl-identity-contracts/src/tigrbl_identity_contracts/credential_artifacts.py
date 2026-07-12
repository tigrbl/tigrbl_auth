"""Format-independent credential, presentation, and verification contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

from tigrbl_identity_core import CredentialFormat, VerificationOutcome


@dataclass(frozen=True, slots=True)
class CredentialArtifact:
    format: CredentialFormat | str
    payload: bytes | str | Mapping[str, Any]
    media_type: str


@dataclass(frozen=True, slots=True)
class PresentationArtifact:
    credentials: Sequence[CredentialArtifact]
    audience: str | None = None
    nonce: str | None = None
    payload: bytes | str | Mapping[str, Any] | None = None
    media_type: str | None = None


@dataclass(frozen=True, slots=True)
class VerificationRequest:
    artifact: CredentialArtifact | PresentationArtifact
    expected_audience: str | None = None
    expected_nonce: str | None = None
    now: int | None = None


@dataclass(frozen=True, slots=True)
class VerificationResult:
    outcome: VerificationOutcome
    claims: Mapping[str, Any] = field(default_factory=dict)
    errors: Sequence[str] = ()
    warnings: Sequence[str] = ()


@runtime_checkable
class CredentialIssuer(Protocol):
    def issue(self, claims: Mapping[str, Any], /, **options: Any) -> CredentialArtifact: ...


@runtime_checkable
class ArtifactVerifier(Protocol):
    def verify(self, request: VerificationRequest, /) -> VerificationResult: ...


@runtime_checkable
class PresentationBuilder(Protocol):
    def present(self, credentials: Sequence[CredentialArtifact], /, **options: Any) -> PresentationArtifact: ...


__all__ = [
    "ArtifactVerifier",
    "CredentialArtifact",
    "CredentialIssuer",
    "PresentationArtifact",
    "PresentationBuilder",
    "VerificationRequest",
    "VerificationResult",
]
