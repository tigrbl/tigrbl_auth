"""Deterministic RFC 7516 compact-JWE structures."""

from dataclasses import dataclass
import json
from typing import Mapping

from tigrbl_identity_core.base64url import base64url_decode


def _decode(segment: str, *, name: str, allow_empty: bool = False) -> bytes:
    if segment == "" and allow_empty:
        return b""
    try:
        if not segment or "=" in segment:
            raise ValueError("empty or padded segment")
        return base64url_decode(segment)
    except (ValueError, UnicodeEncodeError) as exc:
        raise ValueError(f"invalid JWE {name} base64url segment") from exc


@dataclass(frozen=True, slots=True)
class JweCompact:
    serialized: str
    protected_segment: str
    encrypted_key_segment: str
    iv_segment: str
    ciphertext_segment: str
    tag_segment: str
    protected_headers: Mapping[str, object]
    encrypted_key: bytes
    iv: bytes
    ciphertext: bytes
    authentication_tag: bytes

    @property
    def additional_authenticated_data(self) -> bytes:
        return self.protected_segment.encode("ascii")


def parse_jwe_compact(value: str) -> JweCompact:
    if not isinstance(value, str):
        raise TypeError("compact JWE must be text")
    parts = value.split(".")
    if len(parts) != 5 or not parts[0] or not all(parts[index] for index in (2, 3, 4)):
        raise ValueError("compact JWE requires five valid segments")
    try:
        protected = json.loads(_decode(parts[0], name="protected header"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("JWE protected header must be a UTF-8 JSON object") from exc
    if not isinstance(protected, dict):
        raise ValueError("JWE protected header must be a JSON object")
    if not isinstance(protected.get("alg"), str) or not protected["alg"]:
        raise ValueError("JWE protected alg header is required")
    if not isinstance(protected.get("enc"), str) or not protected["enc"]:
        raise ValueError("JWE protected enc header is required")
    return JweCompact(
        value,
        *parts,
        protected,
        _decode(parts[1], name="encrypted key", allow_empty=True),
        _decode(parts[2], name="initialization vector"),
        _decode(parts[3], name="ciphertext"),
        _decode(parts[4], name="authentication tag"),
    )


from .json_serialization import JweJson, JweRecipient, parse_jwe_json

__all__ = ["JweCompact", "JweJson", "JweRecipient", "parse_jwe_compact", "parse_jwe_json"]