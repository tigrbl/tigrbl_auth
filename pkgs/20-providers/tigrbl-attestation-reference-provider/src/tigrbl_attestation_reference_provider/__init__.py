from tigrbl_attestation_bases import ReferenceMaterialProviderBase
from tigrbl_identity_contracts.attestation import ReferenceIntegrityManifest


class InMemoryReferenceMaterialProvider(ReferenceMaterialProviderBase):
    def __init__(self):
        self._manifests: dict[str, ReferenceIntegrityManifest] = {}

    def publish(self, manifest: ReferenceIntegrityManifest) -> None:
        if manifest.tag_identity in self._manifests:
            raise ValueError(f"duplicate reference manifest: {manifest.tag_identity}")
        self._manifests[manifest.tag_identity] = manifest

    def replace(self, manifest: ReferenceIntegrityManifest) -> None:
        self._manifests[manifest.tag_identity] = manifest

    def resolve_manifest(self, tag_identity: str, /) -> ReferenceIntegrityManifest:
        try:
            return self._manifests[tag_identity]
        except KeyError as exc:
            raise LookupError(tag_identity) from exc


__all__ = ["InMemoryReferenceMaterialProvider"]
