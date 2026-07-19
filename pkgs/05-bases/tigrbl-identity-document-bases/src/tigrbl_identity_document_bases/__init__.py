"""Protocol-neutral identity-document extension bases."""

from abc import ABC

from tigrbl_identity_document_contracts import (
    IdentityDocument,
    IdentityDocumentPublisherPort,
    IdentityDocumentResolverPort,
    IdentityDocumentVerificationRequest,
    IdentityDocumentVerificationResult,
    IdentityDocumentVerifierPort,
)


class IdentityDocumentResolverBase(IdentityDocumentResolverPort, ABC):
    def resolve(self, identifier: str, /) -> IdentityDocument:
        raise NotImplementedError


class IdentityDocumentPublisherBase(IdentityDocumentPublisherPort, ABC):
    def publish(self, document: IdentityDocument, /) -> object:
        raise NotImplementedError


class IdentityDocumentVerifierBase(IdentityDocumentVerifierPort, ABC):
    def verify(
        self,
        request: IdentityDocumentVerificationRequest,
        /,
    ) -> IdentityDocumentVerificationResult:
        raise NotImplementedError


__all__ = [
    "IdentityDocumentPublisherBase",
    "IdentityDocumentResolverBase",
    "IdentityDocumentVerifierBase",
]