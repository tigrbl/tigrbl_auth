from dataclasses import dataclass
import json
from typing import Mapping
from tigrbl_identity_core.base64url import base64url_decode


@dataclass(frozen=True, slots=True)
class JwsJsonSignature:
    protected_segment: str
    protected_headers: Mapping[str, object]
    unprotected_headers: Mapping[str, object]
    signature: bytes


@dataclass(frozen=True, slots=True)
class JwsJson:
    payload_segment: str | None
    payload: bytes | None
    signatures: tuple[JwsJsonSignature, ...]


def _signature(value: Mapping[str, object]) -> JwsJsonSignature:
    protected_segment = str(value.get("protected", ""))
    protected = (
        json.loads(base64url_decode(protected_segment)) if protected_segment else {}
    )
    unprotected = value.get("header", {})
    if not isinstance(protected, Mapping) or not isinstance(unprotected, Mapping):
        raise ValueError("JWS headers must be objects")
    if set(protected).intersection(unprotected):
        raise ValueError("JWS protected and unprotected headers collide")
    signature = value.get("signature")
    if not isinstance(signature, str) or not signature:
        raise ValueError("JWS signature is required")
    return JwsJsonSignature(
        protected_segment,
        dict(protected),
        dict(unprotected),
        base64url_decode(signature),
    )


def parse_jws_json(value: str | bytes | Mapping[str, object]) -> JwsJson:
    decoded = json.loads(value) if isinstance(value, (str, bytes)) else dict(value)
    payload_segment = decoded.get("payload")
    if payload_segment is not None and not isinstance(payload_segment, str):
        raise ValueError("JWS payload must be base64url text")
    raw_signatures = decoded.get("signatures")
    if raw_signatures is None:
        raw_signatures = [
            {
                key: decoded[key]
                for key in ("protected", "header", "signature")
                if key in decoded
            }
        ]
    if not isinstance(raw_signatures, list) or not raw_signatures:
        raise ValueError("JWS signatures are required")
    signatures = tuple(
        _signature(item) for item in raw_signatures if isinstance(item, Mapping)
    )
    if len(signatures) != len(raw_signatures):
        raise ValueError("JWS signatures must be objects")
    payload = base64url_decode(payload_segment) if payload_segment else None
    return JwsJson(payload_segment, payload, signatures)
