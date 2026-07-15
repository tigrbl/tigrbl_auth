"""Strict decoder for the WebAuthn authenticator data byte sequence."""

from __future__ import annotations

import io
from dataclasses import dataclass
from enum import IntFlag
from hmac import compare_digest

import cbor2

from ..errors import WebAuthnVerificationError

MAX_AUTHENTICATOR_DATA_BYTES = 65_536


class AuthenticatorDataFlags(IntFlag):
    USER_PRESENT = 0x01
    USER_VERIFIED = 0x04
    BACKUP_ELIGIBLE = 0x08
    BACKUP_STATE = 0x10
    ATTESTED_CREDENTIAL_DATA = 0x40
    EXTENSION_DATA = 0x80


@dataclass(frozen=True, slots=True)
class AttestedCredentialData:
    aaguid: bytes
    credential_id: bytes
    credential_public_key: bytes


@dataclass(frozen=True, slots=True)
class AuthenticatorData:
    raw: bytes
    rp_id_hash: bytes
    flags: AuthenticatorDataFlags
    sign_count: int
    attested_credential_data: AttestedCredentialData | None = None
    extensions: object | None = None

    @property
    def user_present(self) -> bool:
        return bool(self.flags & AuthenticatorDataFlags.USER_PRESENT)

    @property
    def user_verified(self) -> bool:
        return bool(self.flags & AuthenticatorDataFlags.USER_VERIFIED)

    def matches_rp_id_hash(self, expected: bytes) -> bool:
        return len(expected) == 32 and compare_digest(self.rp_id_hash, expected)


def _decode_one(data: bytes, offset: int) -> tuple[object, int]:
    stream = io.BytesIO(data[offset:])
    try:
        value = cbor2.CBORDecoder(stream).decode()
    except Exception as exc:
        raise WebAuthnVerificationError(
            "authenticator data contains invalid CBOR"
        ) from exc
    return value, offset + stream.tell()


def decode_authenticator_data(raw: bytes) -> AuthenticatorData:
    if (
        not isinstance(raw, bytes)
        or len(raw) < 37
        or len(raw) > MAX_AUTHENTICATOR_DATA_BYTES
    ):
        raise WebAuthnVerificationError("authenticator data has an invalid size")
    flags = AuthenticatorDataFlags(raw[32])
    if bool(flags & AuthenticatorDataFlags.BACKUP_STATE) and not bool(
        flags & AuthenticatorDataFlags.BACKUP_ELIGIBLE
    ):
        raise WebAuthnVerificationError(
            "backup state cannot be set for an ineligible credential"
        )
    offset = 37
    attested = None
    if flags & AuthenticatorDataFlags.ATTESTED_CREDENTIAL_DATA:
        if len(raw) < offset + 18:
            raise WebAuthnVerificationError("attested credential data is truncated")
        aaguid = raw[offset : offset + 16]
        credential_id_length = int.from_bytes(raw[offset + 16 : offset + 18], "big")
        offset += 18
        if credential_id_length == 0 or len(raw) < offset + credential_id_length:
            raise WebAuthnVerificationError("attested credential identifier is invalid")
        credential_id = raw[offset : offset + credential_id_length]
        offset += credential_id_length
        _, key_end = _decode_one(raw, offset)
        encoded_key = raw[offset:key_end]
        attested = AttestedCredentialData(aaguid, credential_id, encoded_key)
        offset = key_end
    extensions = None
    if flags & AuthenticatorDataFlags.EXTENSION_DATA:
        extensions, offset = _decode_one(raw, offset)
        if not isinstance(extensions, dict):
            raise WebAuthnVerificationError(
                "authenticator extensions must be a CBOR map"
            )
    if offset != len(raw):
        raise WebAuthnVerificationError("authenticator data contains trailing bytes")
    return AuthenticatorData(
        raw=raw,
        rp_id_hash=raw[:32],
        flags=flags,
        sign_count=int.from_bytes(raw[33:37], "big"),
        attested_credential_data=attested,
        extensions=extensions,
    )


__all__ = [
    "MAX_AUTHENTICATOR_DATA_BYTES",
    "AttestedCredentialData",
    "AuthenticatorData",
    "AuthenticatorDataFlags",
    "decode_authenticator_data",
]
