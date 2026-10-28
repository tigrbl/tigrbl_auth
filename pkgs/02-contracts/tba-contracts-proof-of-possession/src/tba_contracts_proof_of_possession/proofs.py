"""Carrier-neutral possession proofs and contexts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True, slots=True)
class PossessionProofContext:
    audience: str | None = None
    method: str | None = None
    target_uri: str | None = None
    credential_digest: str | None = None
    accompanying_token_digests: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "accompanying_token_digests",
            dict(self.accompanying_token_digests),
        )


@dataclass(frozen=True, slots=True)
class PossessionProof:
    proof_id: str
    artifact: bytes | str
    expires_at: datetime
    context: PossessionProofContext
    profile: str | None = None

    def __post_init__(self) -> None:
        if not self.proof_id:
            raise ValueError("proof id is required")


__all__ = ["PossessionProof", "PossessionProofContext"]