"""Reusable bases for format-specific credential components."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from tigrbl_identity_contracts.credential_artifacts import (
    ArtifactVerifier,
    CredentialArtifact,
    CredentialIssuer,
    PresentationArtifact,
    PresentationBuilder,
    VerificationRequest,
    VerificationResult,
)


class LegacyCredentialIssuerBase(CredentialIssuer, ABC):
    @abstractmethod
    def issue(
        self, claims: Mapping[str, Any], /, **options: Any
    ) -> CredentialArtifact: ...


class LegacyCredentialArtifactVerifierBase(ArtifactVerifier, ABC):
    @abstractmethod
    def verify(self, request: VerificationRequest, /) -> VerificationResult: ...


class LegacyPresentationBuilderBase(PresentationBuilder, ABC):
    @abstractmethod
    def present(
        self, credentials: Sequence[CredentialArtifact], /, **options: Any
    ) -> PresentationArtifact: ...


CredentialIssuerBase = LegacyCredentialIssuerBase
ArtifactVerifierBase = LegacyCredentialArtifactVerifierBase
PresentationBuilderBase = LegacyPresentationBuilderBase

__all__ = [
    "ArtifactVerifierBase",
    "CredentialIssuerBase",
    "LegacyCredentialArtifactVerifierBase",
    "LegacyCredentialIssuerBase",
    "LegacyPresentationBuilderBase",
    "PresentationBuilderBase",
]
