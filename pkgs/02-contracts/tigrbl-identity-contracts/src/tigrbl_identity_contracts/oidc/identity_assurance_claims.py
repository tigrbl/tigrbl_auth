from dataclasses import dataclass
from typing import Final, Mapping


IDENTITY_ASSURANCE_CLAIM_NAMES: Final[tuple[str, ...]] = (
    "verified_claims",
    "place_of_birth",
    "nationalities",
    "birth_family_name",
    "birth_given_name",
    "birth_middle_name",
    "salutation",
    "title",
    "msisdn",
    "also_known_as",
    "address.country_code",
)


@dataclass(frozen=True, slots=True)
class PlaceOfBirth:
    country: str | None = None
    region: str | None = None
    locality: str | None = None


@dataclass(frozen=True, slots=True)
class IdentityAssuranceClaims:
    values: Mapping[str, object]

    def __post_init__(self) -> None:
        unknown = set(self.values) - set(IDENTITY_ASSURANCE_CLAIM_NAMES)
        if unknown:
            raise ValueError(
                f"unregistered identity assurance claims: {sorted(unknown)}"
            )


__all__ = ["IDENTITY_ASSURANCE_CLAIM_NAMES", "IdentityAssuranceClaims", "PlaceOfBirth"]
