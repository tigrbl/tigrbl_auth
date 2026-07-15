"""CollectedClientData parsing and ceremony binding checks."""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from hmac import compare_digest
from urllib.parse import urlsplit

from ..errors import WebAuthnVerificationError
from ..schemas import CollectedClientData

MAX_CLIENT_DATA_BYTES = 16_384


def _b64url_decode(value: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise WebAuthnVerificationError(
            "client challenge must be a non-empty base64url string"
        )
    try:
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except Exception as exc:
        raise WebAuthnVerificationError(
            "client challenge is not valid base64url"
        ) from exc


def _validated_origin(value: object) -> str:
    if not isinstance(value, str):
        raise WebAuthnVerificationError("client origin must be a string")
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"https", "http"}
        or not parsed.hostname
        or parsed.path not in {"", "/"}
    ):
        raise WebAuthnVerificationError("client origin is not a valid web origin")
    if parsed.scheme == "http" and parsed.hostname not in {
        "localhost",
        "127.0.0.1",
        "::1",
    }:
        raise WebAuthnVerificationError("WebAuthn requires HTTPS outside localhost")
    return f"{parsed.scheme}://{parsed.netloc}"


@dataclass(frozen=True, slots=True)
class ParsedClientData:
    value: CollectedClientData
    raw_json: bytes
    digest: bytes
    challenge: bytes


def parse_client_data(
    raw_json: bytes,
    *,
    expected_type: str,
    expected_challenge: bytes,
    expected_origin: str,
) -> ParsedClientData:
    if (
        not isinstance(raw_json, bytes)
        or not raw_json
        or len(raw_json) > MAX_CLIENT_DATA_BYTES
    ):
        raise WebAuthnVerificationError(
            "clientDataJSON is empty or exceeds the supported size"
        )
    try:
        payload = json.loads(raw_json)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WebAuthnVerificationError(
            "clientDataJSON is not valid UTF-8 JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise WebAuthnVerificationError("clientDataJSON must contain an object")
    if payload.get("type") != expected_type:
        raise WebAuthnVerificationError("client data ceremony type does not match")
    challenge = _b64url_decode(payload.get("challenge"))
    if not compare_digest(challenge, expected_challenge):
        raise WebAuthnVerificationError("client data challenge does not match")
    origin = _validated_origin(payload.get("origin"))
    if origin != _validated_origin(expected_origin):
        raise WebAuthnVerificationError("client data origin is not allowed")
    cross_origin = payload.get("crossOrigin", False)
    if not isinstance(cross_origin, bool):
        raise WebAuthnVerificationError("crossOrigin must be boolean")
    top_origin = payload.get("topOrigin")
    if top_origin is not None and not isinstance(top_origin, str):
        raise WebAuthnVerificationError("topOrigin must be a string")
    value = CollectedClientData(
        type=expected_type,
        challenge=payload["challenge"],
        origin=origin,
        cross_origin=cross_origin,
        top_origin=top_origin,
    )
    return ParsedClientData(
        value, raw_json, hashlib.sha256(raw_json).digest(), challenge
    )


__all__ = ["MAX_CLIENT_DATA_BYTES", "ParsedClientData", "parse_client_data"]
