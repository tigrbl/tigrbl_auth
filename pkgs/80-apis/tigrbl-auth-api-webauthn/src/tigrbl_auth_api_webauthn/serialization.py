"""Byte-preserving application/JSON conversion for WebAuthn values."""

from __future__ import annotations

import base64
import re
from dataclasses import fields, is_dataclass
from enum import Enum

from tigrbl_auth_protocol_webauthn import (
    AuthenticatorAssertionResponse,
    AuthenticatorAttestationResponse,
    PublicKeyCredential,
)

from .schemas import PublicKeyCredentialIn


def encode_base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def decode_base64url(value: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise ValueError("a non-empty base64url value is required")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValueError("invalid base64url value")
    try:
        return base64.b64decode(
            value + "=" * (-len(value) % 4), altchars=b"-_", validate=True
        )
    except Exception as exc:
        raise ValueError("invalid base64url value") from exc


def to_json_value(value: object) -> object:
    if isinstance(value, bytes):
        return encode_base64url(value)
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        output: dict[str, object] = {}
        for item in fields(value):
            key = {
                "raw_id": "rawId",
                "rp_id": "rpId",
                "pub_key_cred_params": "pubKeyCredParams",
                "exclude_credentials": "excludeCredentials",
                "allow_credentials": "allowCredentials",
                "authenticator_selection": "authenticatorSelection",
                "authenticator_attachment": "authenticatorAttachment",
                "resident_key": "residentKey",
                "require_resident_key": "requireResidentKey",
                "user_verification": "userVerification",
                "display_name": "displayName",
            }.get(item.name, item.name)
            item_value = getattr(value, item.name)
            if item_value is not None and item_value not in ((), {}):
                output[key] = to_json_value(item_value)
        return output
    if isinstance(value, dict):
        return {str(key): to_json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_json_value(item) for item in value]
    return value


def parse_public_key_credential(value: PublicKeyCredentialIn) -> PublicKeyCredential:
    raw_id = decode_base64url(value.raw_id)
    body = value.response
    if body.attestation_object is not None:
        response = AuthenticatorAttestationResponse(
            client_data_json=decode_base64url(body.client_data_json),
            attestation_object=decode_base64url(body.attestation_object),
            transports=body.transports,
        )
    elif body.authenticator_data is not None and body.signature is not None:
        response = AuthenticatorAssertionResponse(
            client_data_json=decode_base64url(body.client_data_json),
            authenticator_data=decode_base64url(body.authenticator_data),
            signature=decode_base64url(body.signature),
            user_handle=decode_base64url(body.user_handle)
            if body.user_handle
            else None,
        )
    else:
        raise ValueError(
            "credential response is neither attestation nor assertion data"
        )
    return PublicKeyCredential(
        id=value.id,
        raw_id=raw_id,
        response=response,
        type=value.type,
        authenticator_attachment=value.authenticator_attachment,
        client_extension_results=value.client_extension_results,
    )


__all__ = [
    "decode_base64url",
    "encode_base64url",
    "parse_public_key_credential",
    "to_json_value",
]
