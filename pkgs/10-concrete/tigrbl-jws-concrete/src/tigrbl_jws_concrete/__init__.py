"""Deterministic RFC 7515 compact-JWS structures."""

from dataclasses import dataclass
import json
from typing import Mapping

from tigrbl_identity_core.base64url import base64url_decode, base64url_encode


def _decode_segment(segment: str, *, name: str) -> bytes:
    try:
        if "=" in segment:
            raise ValueError("padding is not permitted")
        return base64url_decode(segment)
    except (ValueError, UnicodeEncodeError) as exc:
        raise ValueError(f"invalid {name} base64url segment") from exc


def _decode_header(segment: str) -> Mapping[str, object]:
    try:
        value = json.loads(_decode_segment(segment, name="protected header"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("JWS protected header must be a UTF-8 JSON object") from exc
    if not isinstance(value, dict):
        raise ValueError("JWS protected header must be a JSON object")
    if not isinstance(value.get("alg"), str) or not value["alg"]:
        raise ValueError("JWS protected alg header is required")
    return value


@dataclass(frozen=True, slots=True)
class JwsCompact:
    serialized: str
    protected_segment: str
    payload_segment: str
    signature_segment: str
    protected_headers: Mapping[str, object]
    payload: bytes | None
    signature: bytes

    @property
    def detached(self) -> bool:
        return self.payload_segment == ""

    def signing_input(self, detached_payload: bytes | None = None) -> bytes:
        if self.protected_headers.get("b64", True) is False:
            payload = self.payload if self.payload is not None else detached_payload
            if payload is None:
                raise ValueError("detached unencoded JWS payload is required")
            return self.protected_segment.encode("ascii") + b"." + payload
        payload_segment = self.payload_segment
        if self.detached:
            if detached_payload is None:
                raise ValueError("detached JWS payload is required")
            payload_segment = base64url_encode(detached_payload)
        return f"{self.protected_segment}.{payload_segment}".encode("ascii")


def parse_jws_compact(value: str) -> JwsCompact:
    if not isinstance(value, str):
        raise TypeError("compact JWS must be text")
    parts = value.split(".")
    if len(parts) != 3 or not parts[0] or not parts[2]:
        raise ValueError("compact JWS requires protected, payload, and signature segments")
    protected = _decode_header(parts[0])
    payload = None if parts[1] == "" else _decode_segment(parts[1], name="payload")
    signature = _decode_segment(parts[2], name="signature")
    if not signature:
        raise ValueError("JWS signature must not be empty")
    return JwsCompact(value, parts[0], parts[1], parts[2], protected, payload, signature)


from .json_serialization import JwsJson, JwsJsonSignature, parse_jws_json
from .rfc7797 import validate_unencoded_payload_headers

__all__ = ["JwsCompact", "JwsJson", "JwsJsonSignature", "parse_jws_compact", "parse_jws_json", "validate_unencoded_payload_headers"]