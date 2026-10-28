from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class SdJwtVcTypeMetadata:
    credential_type: str
    name: str | None = None
    description: str | None = None
    extends: str | None = None
    claim_metadata: Sequence[Mapping[str, object]] = ()


def parse_type_metadata(value: Mapping[str, object]) -> SdJwtVcTypeMetadata:
    credential_type = value.get("vct")
    if not isinstance(credential_type, str) or not credential_type:
        raise ValueError("type metadata requires vct")
    claims = value.get("claims", ())
    if not isinstance(claims, list) or not all(
        isinstance(item, Mapping) for item in claims
    ):
        raise ValueError("type metadata claims must be an array of objects")
    extends = value.get("extends")
    if extends is not None and not isinstance(extends, str):
        raise ValueError("extends must be a string")
    return SdJwtVcTypeMetadata(
        credential_type,
        value.get("name") if isinstance(value.get("name"), str) else None,
        value.get("description") if isinstance(value.get("description"), str) else None,
        extends,
        tuple(dict(item) for item in claims),
    )


__all__ = ["SdJwtVcTypeMetadata", "parse_type_metadata"]
