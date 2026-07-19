"""Identity-document extension ports."""

from typing import Protocol

from .documents import IdentityDocument
from .verification import IdentityDocumentVerificationRequest, IdentityDocumentVerificationResult


class IdentityDocumentResolverPort(Protocol):
    def resolve(self, identifier: str, /) -> IdentityDocument: ...


class IdentityDocumentPublisherPort(Protocol):
    def publish(self, document: IdentityDocument, /) -> object: ...


class IdentityDocumentVerifierPort(Protocol):
    def verify(self, request: IdentityDocumentVerificationRequest, /) -> IdentityDocumentVerificationResult: ...


__all__ = ["IdentityDocumentPublisherPort", "IdentityDocumentResolverPort", "IdentityDocumentVerifierPort"]