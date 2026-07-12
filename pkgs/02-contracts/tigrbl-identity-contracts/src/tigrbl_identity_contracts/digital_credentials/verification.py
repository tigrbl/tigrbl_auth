from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence

from .artifacts import DigitalCredential
from .formats import CredentialFormat


@dataclass(frozen=True, slots=True)
class CredentialVerificationRequest:
    credential: DigitalCredential
    expected_format: CredentialFormat
    expected_issuer: str | None = None
    expected_audience: str | None = None


@dataclass(frozen=True, slots=True)
class CredentialVerificationResult:
    valid: bool
    claims: Mapping[str, object] = field(default_factory=dict)
    errors: Sequence[str] = ()


class CredentialFormatVerifierPort(Protocol):
    def verify(
        self, request: CredentialVerificationRequest, /
    ) -> CredentialVerificationResult: ...


__all__ = [
    "CredentialFormatVerifierPort",
    "CredentialVerificationRequest",
    "CredentialVerificationResult",
]
