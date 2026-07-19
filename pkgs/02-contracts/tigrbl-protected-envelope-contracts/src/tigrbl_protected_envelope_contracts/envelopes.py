"""Carrier-neutral signed and encrypted envelope values."""

from dataclasses import dataclass, field
from typing import Mapping

from tigrbl_identity_core import ProtectedEnvelopeKind


@dataclass(frozen=True, slots=True)
class ProtectedEnvelope:
    kind: ProtectedEnvelopeKind
    serialization: bytes | str
    protected_headers: Mapping[object, object] = field(default_factory=dict)
    unprotected_headers: Mapping[object, object] = field(default_factory=dict)
    payload: bytes | None = None
    detached_payload: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ProtectedEnvelopeKind(self.kind))
        object.__setattr__(self, "protected_headers", dict(self.protected_headers))
        object.__setattr__(self, "unprotected_headers", dict(self.unprotected_headers))


__all__ = ["ProtectedEnvelope"]