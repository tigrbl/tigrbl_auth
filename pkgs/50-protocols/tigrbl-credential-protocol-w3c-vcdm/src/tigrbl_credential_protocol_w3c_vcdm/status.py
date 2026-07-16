from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class CredentialStatusEntry:
    identifier: str
    status_type: str
    properties: Mapping[str, object]


def parse_credential_status(value: Mapping[str, object]) -> CredentialStatusEntry:
    identifier, status_type = value.get("id"), value.get("type")
    if (
        not isinstance(identifier, str)
        or not identifier
        or not isinstance(status_type, str)
        or not status_type
    ):
        raise ValueError("credentialStatus requires id and type")
    return CredentialStatusEntry(
        identifier,
        status_type,
        {name: item for name, item in value.items() if name not in {"id", "type"}},
    )


__all__ = ["CredentialStatusEntry", "parse_credential_status"]
