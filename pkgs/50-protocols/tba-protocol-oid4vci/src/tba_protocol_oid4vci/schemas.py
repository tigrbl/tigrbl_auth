"""Typed OID4VCI wire-schema projections."""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Oid4vciCredentialRequest:
    credential_configuration_id: str
    format: str
    proofs: Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class Oid4vciCredentialResponse:
    credential: str | bytes | None = None
    transaction_id: str | None = None


__all__ = ["Oid4vciCredentialRequest", "Oid4vciCredentialResponse"]
