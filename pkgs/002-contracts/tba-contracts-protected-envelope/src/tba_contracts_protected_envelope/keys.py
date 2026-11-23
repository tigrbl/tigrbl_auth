from dataclasses import dataclass, field
from typing import Mapping

@dataclass(frozen=True, slots=True)
class VerificationKeyRequest:
    key_id: str | bytes | None
    algorithm: str | int
    issuer: str | None = None
    profile: str | None = None

@dataclass(frozen=True, slots=True)
class VerificationKeyResult:
    resolved: bool
    key: object | None = None
    key_id: str | bytes | None = None
    trusted: bool = False
    source: str | None = None
    evidence: Mapping[str, object] = field(default_factory=dict)