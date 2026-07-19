"""DID Core parsing, resolution, and verification bindings."""

from tigrbl_did_document_concrete import DidDocument
from tigrbl_identity_document_contracts import (
    IdentityDocumentResolverPort,
    IdentityDocumentVerificationRequest,
    IdentityDocumentVerificationResult,
)

from .validation import validate_document


class DidCoreProtocol:
    def __init__(self, resolver: IdentityDocumentResolverPort | None = None) -> None:
        self._resolver = resolver

    def parse(
        self,
        representation: bytes | str,
        *,
        media_type: str = "application/did+json",
    ) -> DidDocument:
        document = DidDocument.from_representation(
            representation,
            media_type=media_type,
        )
        validate_document(document.content)
        return document

    def verify(
        self,
        request: IdentityDocumentVerificationRequest,
        /,
    ) -> IdentityDocumentVerificationResult:
        document = request.document
        try:
            parsed = self.parse(
                document.representation,
                media_type=document.media_type,
            )
            if (
                request.expected_subject is not None
                and parsed.subject != request.expected_subject
            ):
                raise ValueError("DID Document subject mismatch")
            if (
                request.expected_controller is not None
                and parsed.controller != request.expected_controller
            ):
                raise ValueError("DID Document controller mismatch")
        except (TypeError, ValueError) as exc:
            return IdentityDocumentVerificationResult(False, reason=str(exc))
        return IdentityDocumentVerificationResult(
            True,
            structural_valid=True,
            controller_authorized=True,
            key_material_valid=True,
            representation_valid=True,
            subject=parsed.subject,
            controller=parsed.controller,
            evidence={"did_core_revision": "1.0"},
        )

    def resolve(self, identifier: str, /) -> DidDocument:
        if self._resolver is None:
            raise RuntimeError("DID resolver is not configured")
        document = self._resolver.resolve(identifier)
        result = self.verify(
            IdentityDocumentVerificationRequest(
                document,
                expected_subject=identifier,
            )
        )
        if not result.valid:
            raise ValueError(result.reason or "resolved DID Document is invalid")
        return self.parse(document.representation, media_type=document.media_type)


__all__ = ["DidCoreProtocol"]
