from dataclasses import dataclass
from typing import Mapping

from tigrbl_digital_credential_bases import CredentialFormatBase


@dataclass(frozen=True, slots=True)
class VerifiableCredential(CredentialFormatBase):
    format_identifier = "w3c-vcdm"
    contexts: tuple[object, ...]
    types: tuple[str, ...]
    issuer: str | Mapping[str, object]
    credential_subjects: tuple[Mapping[str, object], ...]
    identifier: str | None = None
    valid_from: str | None = None
    valid_until: str | None = None
    status: tuple[Mapping[str, object], ...] = ()
    schemas: tuple[Mapping[str, object], ...] = ()
    proof: object | None = None


__all__ = ["VerifiableCredential"]
