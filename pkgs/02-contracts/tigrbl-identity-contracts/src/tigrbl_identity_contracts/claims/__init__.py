"""Protocol-neutral individual claim and claim-set contracts."""

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence
from tigrbl_identity_core import ClaimType, ClaimValueType


@dataclass(frozen=True, slots=True)
class Claim:
    name: str
    value: Any
    claim_type: ClaimType
    value_type: ClaimValueType
    standards: tuple[str, ...] = ()
    required: bool = False


@dataclass(frozen=True, slots=True)
class ClaimDescriptor:
    name: str
    source: str = "user"
    essential: bool = False


@dataclass(frozen=True, slots=True)
class ClaimSet:
    claims: tuple[Claim, ...]
    protocol: str | None = None
    version: str | None = None

    def as_mapping(self) -> dict[str, Any]:
        return {claim.name: claim.value for claim in self.claims}

    def get(self, name: str) -> Claim | None:
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
    "ClaimDescriptor",
    "ClaimSet",
    "ClaimSetComposerPort",
    "ClaimValidatorPort",
    "ClaimsProviderPort",
    "ClaimsRequest",
    "ClaimsResult",
]
