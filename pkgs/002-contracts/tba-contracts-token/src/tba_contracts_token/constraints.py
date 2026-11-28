from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SenderConstraint:
    method: str
    confirmation: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ReplayValidation:
    accepted: bool
    token_id: str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class IssuerTrustResult:
    trusted: bool
    issuer: str
    reason: str | None = None


__all__ = ["IssuerTrustResult", "ReplayValidation", "SenderConstraint"]
