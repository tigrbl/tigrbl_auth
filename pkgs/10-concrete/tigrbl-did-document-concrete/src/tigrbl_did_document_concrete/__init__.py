"""Canonical standalone DID Document artifact."""

from __future__ import annotations

import json
from collections.abc import Mapping

from tigrbl_identity_core import IdentityDocumentKind
from tigrbl_identity_document_contracts import IdentityDocument


DID_JSON = "application/did+json"
DID_JSON_LD = "application/did+ld+json"
DID_MEDIA_TYPES = frozenset({DID_JSON, DID_JSON_LD})


class DidDocument(IdentityDocument):
    """A canonical serialized DID Document with carrier-neutral identity semantics."""

    def __init__(
        self,
        identifier: str,
        content: Mapping[str, object],
        *,
        media_type: str = DID_JSON,
        version: str | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> None:
        if media_type not in DID_MEDIA_TYPES:
            raise ValueError(f"unsupported DID Document media type: {media_type}")
        materialized = dict(content)
        if materialized.get("id") != identifier:
            raise ValueError("DID Document id must match its identifier")
        representation = json.dumps(
            materialized,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        controller = materialized.get("controller")
        if isinstance(controller, list):
            controller = controller[0] if controller else identifier
        if not isinstance(controller, str):
            controller = identifier
        super().__init__(
            identifier,
            identifier,
            IdentityDocumentKind.DID_DOCUMENT,
            representation,
            media_type,
            controller,
            version,
            metadata or {},
        )

    @classmethod
    def from_representation(
        cls,
        representation: bytes | str,
        *,
        media_type: str = DID_JSON,
        version: str | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> DidDocument:
        raw = (
            representation.decode("utf-8")
            if isinstance(representation, bytes)
            else representation
        )
        value = json.loads(raw)
        if not isinstance(value, dict) or not isinstance(value.get("id"), str):
            raise ValueError("DID Document representation must be an object with an id")
        return cls(
            value["id"],
            value,
            media_type=media_type,
            version=version,
            metadata=metadata,
        )

    @property
    def content(self) -> Mapping[str, object]:
        value = json.loads(self.representation)
        if not isinstance(value, dict):
            raise ValueError("DID Document representation must be an object")
        return value


__all__ = ["DID_JSON", "DID_JSON_LD", "DID_MEDIA_TYPES", "DidDocument"]
