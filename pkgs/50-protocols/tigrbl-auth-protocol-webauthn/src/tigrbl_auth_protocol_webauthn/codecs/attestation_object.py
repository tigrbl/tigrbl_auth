"""Decoder for WebAuthn attestation objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import cbor2

from ..errors import WebAuthnVerificationError
from .authenticator_data import AuthenticatorData, decode_authenticator_data

MAX_ATTESTATION_OBJECT_BYTES = 131_072


@dataclass(frozen=True, slots=True)
class AttestationObject:
    format: str
    authenticator_data: AuthenticatorData
    statement: Mapping[object, object]


def decode_attestation_object(encoded: bytes) -> AttestationObject:
    if (
        not isinstance(encoded, bytes)
        or not encoded
        or len(encoded) > MAX_ATTESTATION_OBJECT_BYTES
    ):
        raise WebAuthnVerificationError(
            "attestation object is empty or exceeds the supported size"
        )
    try:
        value = cbor2.loads(encoded)
    except Exception as exc:
        raise WebAuthnVerificationError("attestation object is not valid CBOR") from exc
    if not isinstance(value, dict) or set(value) != {"fmt", "authData", "attStmt"}:
        raise WebAuthnVerificationError(
            "attestation object must contain fmt, authData, and attStmt"
        )
    if not isinstance(value["fmt"], str) or not isinstance(value["authData"], bytes):
        raise WebAuthnVerificationError("attestation object fields have invalid types")
    if not isinstance(value["attStmt"], dict):
        raise WebAuthnVerificationError("attestation statement must be a CBOR map")
    return AttestationObject(
        format=value["fmt"],
        authenticator_data=decode_authenticator_data(value["authData"]),
        statement=value["attStmt"],
    )


__all__ = [
    "MAX_ATTESTATION_OBJECT_BYTES",
    "AttestationObject",
    "decode_attestation_object",
]
