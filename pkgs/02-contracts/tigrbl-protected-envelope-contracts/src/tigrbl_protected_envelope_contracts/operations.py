"""Protected-envelope operation requests and results."""

from dataclasses import dataclass
from typing import Mapping

from tigrbl_identity_core import ProtectedEnvelopeKind

from .envelopes import ProtectedEnvelope


@dataclass(frozen=True, slots=True)
class EnvelopeProtectionRequest:
    kind: ProtectedEnvelopeKind
    payload: bytes
    protected_headers: Mapping[object, object]
    key_reference: str


@dataclass(frozen=True, slots=True)
class EnvelopeVerificationRequest:
    envelope: ProtectedEnvelope
    detached_payload: bytes | None = None
    expected_profile: str | None = None


@dataclass(frozen=True, slots=True)
class EnvelopeVerificationResult:
    valid: bool
    payload: bytes | None = None
    key_reference: str | None = None
    reason: str | None = None


__all__ = ["EnvelopeProtectionRequest", "EnvelopeVerificationRequest", "EnvelopeVerificationResult"]