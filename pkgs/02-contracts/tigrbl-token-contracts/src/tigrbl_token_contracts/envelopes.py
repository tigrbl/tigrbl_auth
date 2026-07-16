from dataclasses import dataclass
from typing import Mapping

from .profiles import TokenEnvelopeFormat, TokenProfile


@dataclass(frozen=True, slots=True)
class ProtectedTokenEnvelope:
    serialized: str | bytes
    format: TokenEnvelopeFormat
    profile: TokenProfile


@dataclass(frozen=True, slots=True)
class VerifiedTokenEnvelope:
    envelope: ProtectedTokenEnvelope
    claims: Mapping[str | int, object]
    key_id: str | None = None
    algorithm: str | int | None = None


__all__ = ["ProtectedTokenEnvelope", "VerifiedTokenEnvelope"]
