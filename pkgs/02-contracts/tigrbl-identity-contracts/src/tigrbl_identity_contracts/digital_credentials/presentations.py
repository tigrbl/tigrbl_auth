from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence

from .artifacts import DigitalCredential


@dataclass(frozen=True, slots=True)
class DisclosureSelection:
    claim_paths: Sequence[str]


@dataclass(frozen=True, slots=True)
class HolderBinding:
    method: str
    key_reference: str | None = None


@dataclass(frozen=True, slots=True)
class TransactionBinding:
    nonce: str
    audience: str
    transaction_id: str | None = None

    @property
    def replay_value(self) -> str:
        """Normalized replay value independent of the originating wire name."""
        return self.transaction_id or self.nonce


@dataclass(frozen=True, slots=True)
class PresentationRequest:
    accepted_formats: Sequence[str]
    binding: TransactionBinding
    requested_claims: Sequence[str] = ()


@dataclass(frozen=True, slots=True)
class PresentationResult:
    valid: bool
    credentials: Sequence[DigitalCredential] = ()
    disclosed_claims: Mapping[str, object] = field(default_factory=dict)
    errors: Sequence[str] = ()


class PresentationVerifierPort(Protocol):
    def verify(
        self, presentation: bytes | str, request: PresentationRequest, /
    ) -> PresentationResult: ...


__all__ = [
    "DisclosureSelection",
    "HolderBinding",
    "PresentationRequest",
    "PresentationResult",
    "PresentationVerifierPort",
    "TransactionBinding",
]
