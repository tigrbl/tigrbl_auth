from collections.abc import Mapping

from tigrbl_corim_concrete import (
    CorimTag,
    parse_corim,
    parse_corim_tag,
    validate_corim_tag,
)
from tigrbl_identity_contracts.attestation import ReferenceIntegrityManifest


class InMemoryCorimStore:
    def __init__(self):
        self._tags: dict[str, CorimTag] = {}
        self._manifests: dict[str, ReferenceIntegrityManifest] = {}

    def publish(self, value: Mapping[str, object]) -> CorimTag:
        tag = parse_corim_tag(value)
        validate_corim_tag(tag)
        identifier = str(tag.tag_identity)
        if identifier in self._tags:
            raise ValueError(f"CoRIM tag is immutable once published: {identifier}")
        self._tags[identifier] = tag
        self._manifests[identifier] = parse_corim(value)
        return tag

    def get(self, tag_identity: str) -> CorimTag:
        try:
            return self._tags[tag_identity]
        except KeyError as exc:
            raise LookupError(tag_identity) from exc

    def resolve_manifest(self, tag_identity: str, /) -> ReferenceIntegrityManifest:
        try:
            return self._manifests[tag_identity]
        except KeyError as exc:
            raise LookupError(tag_identity) from exc


__all__ = ["InMemoryCorimStore"]
