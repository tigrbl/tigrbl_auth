from dataclasses import dataclass
from typing import Mapping, Sequence

from .contexts import validate_contexts


@dataclass(frozen=True, slots=True)
class VerifiablePresentation:
    contexts: tuple[object, ...]
    types: tuple[str, ...]
    credentials: tuple[object, ...] = ()
    holder: str | Mapping[str, object] | None = None
    identifier: str | None = None
    proof: object | None = None


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


__all__ = ["VerifiablePresentation", "parse_verifiable_presentation"]
