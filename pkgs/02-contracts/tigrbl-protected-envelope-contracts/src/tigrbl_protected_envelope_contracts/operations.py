from dataclasses import dataclass, field
from typing import Mapping
from tigrbl_identity_core import ProtectedEnvelopeKind
from .envelopes import ProtectedEnvelope

@dataclass(frozen=True, slots=True)
class EnvelopeProtectionRequest:
    kind: ProtectedEnvelopeKind
    payload: bytes
    protected_headers: Mapping[object, object]
    key_reference: str
    profile: str | None = None
    external_aad: bytes = b""

@dataclass(frozen=True, slots=True)
class EnvelopeVerificationRequest:
    envelope: ProtectedEnvelope
    detached_payload: bytes | None = None
    expected_profile: str | None = None
    expected_issuer: str | None = None
    expected_audience: str | None = None
    external_aad: bytes = b""

@dataclass(frozen=True, slots=True)
class EnvelopeVerificationResult:
    valid: bool
    structural_valid: bool = False
    cryptographic_valid: bool = False
    key_resolved: bool = False
    issuer_trusted: bool = False
    profile_valid: bool = False
    time_valid: bool | None = None
    replay_valid: bool | None = None
    payload: bytes | None = None
    key_reference: str | None = None
    reason: str | None = None
    evidence: Mapping[str, object] = field(default_factory=dict)