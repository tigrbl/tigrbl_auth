"""Decentralized identifier and resolution contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class Did:
    method: str
    method_specific_id: str

    @classmethod
    def parse(cls, value: str) -> "Did":
        parts = value.split(":", 2)
        if len(parts) != 3 or parts[0] != "did" or not all(parts[1:]):
            raise ValueError("invalid DID")
        return cls(parts[1], parts[2])

    def __str__(self) -> str:
        return f"did:{self.method}:{self.method_specific_id}"


@dataclass(frozen=True, slots=True)
class DidResolutionResult:
    did_document: Mapping[str, Any] | None
    resolution_metadata: Mapping[str, Any]
    document_metadata: Mapping[str, Any]


class DidResolver(Protocol):
    def resolve(self, did: Did, /) -> DidResolutionResult: ...


__all__ = ["Did", "DidResolutionResult", "DidResolver"]
