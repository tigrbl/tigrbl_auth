from typing import Mapping, Sequence

from tigrbl_verifiable_credential_concrete import VerifiableCredential
from tigrbl_verifiable_presentation_concrete import VerifiablePresentation

from .contexts import validate_contexts
from .schema_references import parse_credential_schema
from .status import parse_credential_status


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


def parse_verifiable_presentation(
    value: Mapping[str, object],
) -> VerifiablePresentation:
    contexts = validate_contexts(value.get("@context"))
    types = value.get("type")
    if (
        not isinstance(types, list)
        or "VerifiablePresentation" not in types
        or not all(isinstance(item, str) for item in types)
    ):
        raise ValueError("type must include VerifiablePresentation")
    credentials = value.get("verifiableCredential", ())
    if isinstance(credentials, (str, Mapping)):
        credentials = (credentials,)
    if (
        not isinstance(credentials, Sequence)
        or isinstance(credentials, bytes)
        or any(not isinstance(item, (str, Mapping)) for item in credentials)
    ):
        raise ValueError(
            "verifiableCredential must contain credential objects or strings"
        )
    holder = value.get("holder")
    if holder is not None and not isinstance(holder, (str, Mapping)):
        raise ValueError("holder must be a URL or object")
    return VerifiablePresentation(
        contexts,
        tuple(types),
        tuple(credentials),
        holder,
        value.get("id") if isinstance(value.get("id"), str) else None,
        value.get("proof"),
    )


__all__ = ["parse_verifiable_credential", "parse_verifiable_presentation"]
