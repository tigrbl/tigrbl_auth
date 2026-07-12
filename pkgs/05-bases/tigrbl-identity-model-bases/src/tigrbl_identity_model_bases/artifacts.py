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


class CredentialIssuerBase(CredentialIssuer, ABC):
    @abstractmethod
    def issue(
        self, claims: Mapping[str, Any], /, **options: Any
    ) -> CredentialArtifact: ...


class ArtifactVerifierBase(ArtifactVerifier, ABC):
    @abstractmethod
    def verify(self, request: VerificationRequest, /) -> VerificationResult: ...


class PresentationBuilderBase(PresentationBuilder, ABC):
    @abstractmethod
    def present(
        self, credentials: Sequence[CredentialArtifact], /, **options: Any
    ) -> PresentationArtifact: ...


__all__ = ["ArtifactVerifierBase", "CredentialIssuerBase", "PresentationBuilderBase"]
