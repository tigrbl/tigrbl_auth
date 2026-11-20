from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class AssuranceEvidence:
    type: str
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.type.strip():
            raise ValueError("assurance evidence type must not be empty")


@dataclass(frozen=True, slots=True)
class VerificationMetadata:
    trust_framework: str
    assurance_level: str | None = None
    assurance_process: Mapping[str, Any] | None = None
    time: str | None = None
    verification_process: str | None = None
    evidence: Sequence[AssuranceEvidence] = ()

    def __post_init__(self) -> None:
        if not self.trust_framework.strip():
            raise ValueError("trust_framework must not be empty")


@dataclass(frozen=True, slots=True)
class VerifiedClaims:
    verification: VerificationMetadata
    claims: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class VerifiedClaimsRequest:
    claims: Mapping[str, Any]
    verification: Mapping[str, Any] = field(default_factory=dict)


__all__ = [
    "AssuranceEvidence",
    "VerificationMetadata",
    "VerifiedClaims",
    "VerifiedClaimsRequest",
]
