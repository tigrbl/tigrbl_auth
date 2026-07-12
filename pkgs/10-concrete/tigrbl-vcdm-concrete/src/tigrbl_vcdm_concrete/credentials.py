from dataclasses import dataclass
from typing import Mapping, Sequence

from .contexts import validate_contexts
from .schemas import CredentialSchemaReference, parse_credential_schema
from .status import CredentialStatusEntry, parse_credential_status


@dataclass(frozen=True, slots=True)
class VerifiableCredential:
    contexts: tuple[object, ...]
    types: tuple[str, ...]
    issuer: str | Mapping[str, object]
    credential_subjects: tuple[Mapping[str, object], ...]
    identifier: str | None = None
    valid_from: str | None = None
    valid_until: str | None = None
    status: tuple[CredentialStatusEntry, ...] = ()
    schemas: tuple[CredentialSchemaReference, ...] = ()
    proof: object | None = None


def _objects(value: object, name: str) -> tuple[Mapping[str, object], ...]:
    values = (value,) if isinstance(value, Mapping) else value
    if (
        not isinstance(values, Sequence)
        or isinstance(values, (str, bytes))
        or not values
        or not all(isinstance(item, Mapping) for item in values)
    ):
        raise ValueError(f"{name} must be an object or non-empty array of objects")
    return tuple(dict(item) for item in values)


def parse_verifiable_credential(value: Mapping[str, object]) -> VerifiableCredential:
    contexts = validate_contexts(value.get("@context"))
    types, issuer = value.get("type"), value.get("issuer")
    if (
        not isinstance(types, list)
        or "VerifiableCredential" not in types
        or not all(isinstance(item, str) for item in types)
    ):
        raise ValueError("type must include VerifiableCredential")
    if not isinstance(issuer, (str, Mapping)) or not issuer:
        raise ValueError("credential requires issuer")
    subjects = _objects(value.get("credentialSubject"), "credentialSubject")
    statuses = (
        tuple(
            parse_credential_status(item)
            for item in _objects(value["credentialStatus"], "credentialStatus")
        )
        if "credentialStatus" in value
        else ()
    )
    schemas = (
        tuple(
            parse_credential_schema(item)
            for item in _objects(value["credentialSchema"], "credentialSchema")
        )
        if "credentialSchema" in value
        else ()
    )
    return VerifiableCredential(
        contexts,
        tuple(types),
        issuer,
        subjects,
        value.get("id") if isinstance(value.get("id"), str) else None,
        value.get("validFrom") if isinstance(value.get("validFrom"), str) else None,
        value.get("validUntil") if isinstance(value.get("validUntil"), str) else None,
        statuses,
        schemas,
        value.get("proof"),
    )


__all__ = ["VerifiableCredential", "parse_verifiable_credential"]
