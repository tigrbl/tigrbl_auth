"""Protocol-neutral individual claim and claim-set contracts."""

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence
from tigrbl_identity_core import (
    ClaimDisclosureMode,
    ClaimIdentifier,
    ClaimLabel,
    ClaimNameKind,
    ClaimSourceKind,
    ClaimType,
    ClaimValueType,
)


@dataclass(frozen=True, slots=True)
class ClaimProvenance:
    source_kind: ClaimSourceKind
    source_id: str | None = None
    evidence_reference: str | None = None
    verified_at: str | None = None
    assurance_framework: str | None = None


@dataclass(frozen=True, slots=True)
class ClaimDisclosure:
    mode: ClaimDisclosureMode = ClaimDisclosureMode.REQUESTED
    purpose: str | None = None
    consent_reference: str | None = None


@dataclass(frozen=True, slots=True)
class Claim:
    name: ClaimLabel
    value: Any
    claim_type: ClaimType
    value_type: ClaimValueType
    standards: tuple[str, ...] = ()
    required: bool = False
    name_kind: ClaimNameKind = ClaimNameKind.SPECIFICATION
    namespace: str | None = None
    registry: str | None = None
    provenance: ClaimProvenance | None = None
    disclosure: ClaimDisclosure | None = None

    @property
    def identifier(self) -> ClaimIdentifier:
        return ClaimIdentifier(self.name, self.name_kind, self.namespace, self.registry)


@dataclass(frozen=True, slots=True)
class ClaimDescriptor:
    name: ClaimLabel
    source: str = "user"
    essential: bool = False


@dataclass(frozen=True, slots=True)
class ClaimSet:
    claims: tuple[Claim, ...]
    protocol: str | None = None
    version: str | None = None

    def as_mapping(self) -> dict[ClaimLabel, Any]:
        return {claim.name: claim.value for claim in self.claims}

    def get(self, name: ClaimLabel) -> Claim | None:
        return next((claim for claim in self.claims if claim.name == name), None)


@dataclass(frozen=True, slots=True)
class ClaimsRequest:
    subject: str
    scopes: tuple[str, ...] = ()
    requested_claims: tuple[ClaimDescriptor, ...] = ()
    user: Any | None = None
    session: Any | None = None
    consents: tuple[Any, ...] = ()
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ClaimsResult:
    claims: Mapping[str, Any] | ClaimSet
    omitted: tuple[str, ...] = ()


class ClaimValidatorPort(Protocol):
    def validate(self, claim: Claim, /) -> None: ...


class ClaimsProviderPort(Protocol):
    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult: ...


class ClaimSetComposerPort(Protocol):
    def compose(
        self, claims: Sequence[Claim], /, *, protocol: str, version: str
    ) -> ClaimSet: ...


__all__ = [
    "Claim",
    "ClaimDisclosure",
    "ClaimDescriptor",
    "ClaimProvenance",
    "ClaimSet",
    "ClaimSetComposerPort",
    "ClaimValidatorPort",
    "ClaimsProviderPort",
    "ClaimsRequest",
    "ClaimsResult",
]
