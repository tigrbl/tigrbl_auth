from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class CredentialSchemaReference:
    identifier: str
    schema_type: str
    properties: Mapping[str, object]


def parse_credential_schema(value: Mapping[str, object]) -> CredentialSchemaReference:
    identifier, schema_type = value.get("id"), value.get("type")
    if (
        not isinstance(identifier, str)
        or not identifier
        or not isinstance(schema_type, str)
        or not schema_type
    ):
        raise ValueError("credentialSchema requires id and type")
    return CredentialSchemaReference(
        identifier,
        schema_type,
        {name: item for name, item in value.items() if name not in {"id", "type"}},
    )


__all__ = ["CredentialSchemaReference", "parse_credential_schema"]
