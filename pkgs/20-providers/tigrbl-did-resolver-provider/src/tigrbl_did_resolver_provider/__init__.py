from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from tigrbl_did_concrete import select_document_resource, validate_did_document
from tigrbl_identity_contracts.did import (
    Did,
    DidDereferencingResult,
    DidDocument,
    DidResolutionResult,
    DidUrl,
)
from tigrbl_security_trust_domain_bases import DidResolverBase

MethodResolver = Callable[[Did], DidDocument]


@dataclass(frozen=True, slots=True)
class DidDocumentVersion:
    version_id: str
    document: DidDocument
    published_at: datetime


class VersionedDidResolverProvider(DidResolverBase):
    def __init__(self):
        self._methods: dict[str, MethodResolver] = {}
        self._versions: dict[Did, list[DidDocumentVersion]] = {}

    def register_method(self, method: str, resolver: MethodResolver) -> None:
        if not method or method in self._methods:
            raise ValueError("DID method resolver must be non-empty and unique")
        self._methods[method] = resolver

    def publish(self, document: DidDocument, version_id: str) -> DidDocumentVersion:
        validate_did_document(document)
        versions = self._versions.setdefault(document.identifier, [])
        if not version_id or any(
            version.version_id == version_id for version in versions
        ):
            raise ValueError("DID document version must be non-empty and unique")
        version = DidDocumentVersion(version_id, document, datetime.now(timezone.utc))
        versions.append(version)
        return version

    def resolve(self, did: Did, /) -> DidResolutionResult:
        versions = self._versions.get(did)
        if versions:
            latest = versions[-1]
            return DidResolutionResult(
                latest.document,
                {"source": "authoritative-cache"},
                {
                    "versionId": latest.version_id,
                    "updated": latest.published_at.isoformat(),
                },
            )
        resolver = self._methods.get(did.method)
        if resolver is None:
            return DidResolutionResult(None, {"error": "methodNotSupported"}, {})
        try:
            document = resolver(did)
            validate_did_document(document)
        except (LookupError, ValueError) as exc:
            return DidResolutionResult(
                None, {"error": "notFound", "detail": str(exc)}, {}
            )
        if document.identifier != did:
            return DidResolutionResult(None, {"error": "invalidDidDocument"}, {})
        return DidResolutionResult(document, {"source": "method-resolver"}, {})

    def dereference(self, did_url: DidUrl, /) -> DidDereferencingResult:
        resolution = self.resolve(did_url.did)
        if resolution.document is None:
            return DidDereferencingResult(None, resolution.resolution_metadata, {})
        try:
            content = select_document_resource(resolution.document, did_url)
        except LookupError:
            return DidDereferencingResult(None, {"error": "notFound"}, {})
        return DidDereferencingResult(content, {}, resolution.document_metadata)


__all__ = ["DidDocumentVersion", "MethodResolver", "VersionedDidResolverProvider"]
