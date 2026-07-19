"""Carrier-neutral identity-document values."""

from dataclasses import dataclass, field
from typing import Mapping

from tigrbl_identity_core import IdentityDocumentKind


@dataclass(frozen=True, slots=True)
class IdentityDocument:
    document_id: str
    subject: str
    kind: IdentityDocumentKind
    representation: bytes | str
    media_type: str
    controller: str | None = None
    version: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.document_id or not self.subject or not self.media_type:
            raise ValueError("identity document id, subject, and media type are required")
        object.__setattr__(self, "kind", IdentityDocumentKind(self.kind))
        object.__setattr__(self, "metadata", dict(self.metadata))


__all__ = ["IdentityDocument"]