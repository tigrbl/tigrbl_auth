"""Canonical digital credential issuance contracts."""

from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence

from .artifacts import DigitalCredential
from .formats import CredentialFormat, CredentialType


@dataclass(frozen=True, slots=True)
class CredentialConfiguration:
    identifier: str
    credential_type: CredentialType
    supported_formats: Sequence[CredentialFormat]


@dataclass(frozen=True, slots=True)
class CredentialOffer:
    issuer: str
    configuration_ids: Sequence[str]
    transaction_code_required: bool = False


@dataclass(frozen=True, slots=True)
class CredentialIssuanceRequest:
    configuration_id: str
    format: CredentialFormat
    subject: str | None = None
    proof: bytes | str | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CredentialIssuanceResult:
    credential: DigitalCredential | None = None
    transaction_id: str | None = None
    notification_id: str | None = None


class CredentialIssuerPort(Protocol):
    def issue(
        self, request: CredentialIssuanceRequest, /
    ) -> CredentialIssuanceResult: ...


__all__ = [
    "CredentialConfiguration",
    "CredentialIssuanceRequest",
    "CredentialIssuanceResult",
    "CredentialIssuerPort",
    "CredentialOffer",
]
