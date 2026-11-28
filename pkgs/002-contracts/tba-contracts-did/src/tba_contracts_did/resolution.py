"""Canonical DID resolution contracts."""

from dataclasses import dataclass, field
from typing import Mapping, Protocol

from .documents import DidDocument
from .identifiers import Did, DidUrl


@dataclass(frozen=True, slots=True)
class DidResolutionResult:
    document: DidDocument | None
    resolution_metadata: Mapping[str, object] = field(default_factory=dict)
    document_metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DidDereferencingResult:
    content: object | None
    dereferencing_metadata: Mapping[str, object] = field(default_factory=dict)
    content_metadata: Mapping[str, object] = field(default_factory=dict)


class DidResolverPort(Protocol):
    def resolve(self, did: Did, /) -> DidResolutionResult: ...

    def dereference(self, did_url: DidUrl, /) -> DidDereferencingResult: ...


__all__ = ["DidDereferencingResult", "DidResolutionResult", "DidResolverPort"]
