"""Identity-document verification requests and results."""

from dataclasses import dataclass, field
from typing import Mapping

from .documents import IdentityDocument


@dataclass(frozen=True, slots=True)
class IdentityDocumentVerificationRequest:
    document: IdentityDocument
    expected_subject: str | None = None
    expected_controller: str | None = None


@dataclass(frozen=True, slots=True)
class IdentityDocumentVerificationResult:
    valid: bool
    subject: str | None = None
    controller: str | None = None
    reason: str | None = None
    evidence: Mapping[str, object] = field(default_factory=dict)


__all__ = ["IdentityDocumentVerificationRequest", "IdentityDocumentVerificationResult"]