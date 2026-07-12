"""Standalone structural SD-JWT VC concrete."""

from __future__ import annotations
import base64
import json
from dataclasses import dataclass
from typing import Any, Mapping

MEDIA_TYPE = "application/dc+sd-jwt"
TYP = "dc+sd-jwt"


def _decode_json(segment: str) -> Mapping[str, Any]:
    value = json.loads(base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4)))
    if not isinstance(value, dict):
        raise ValueError("JWT segment must contain a JSON object")
    return value


@dataclass(frozen=True, slots=True)
class SdJwtVc:
    issuer_jwt: str
    disclosures: tuple[str, ...]
    key_binding_jwt: str | None
    header: Mapping[str, Any]
    claims: Mapping[str, Any]


def parse_sd_jwt_vc(value: str) -> SdJwtVc:
    parts = value.split("~")
    jwt_parts = parts[0].split(".")
    if len(jwt_parts) != 3:
        raise ValueError("SD-JWT VC must begin with a compact JWS")
    header, claims = _decode_json(jwt_parts[0]), _decode_json(jwt_parts[1])
    if header.get("typ") != TYP:
        raise ValueError(f"SD-JWT VC typ must be {TYP!r}")
    if not isinstance(claims.get("vct"), str):
        raise ValueError("SD-JWT VC requires the vct claim")
    tail = [item for item in parts[1:] if item]
    key_binding = tail.pop() if tail and tail[-1].count(".") == 2 else None
    return SdJwtVc(parts[0], tuple(tail), key_binding, header, claims)


__all__ = ["MEDIA_TYPE", "SdJwtVc", "TYP", "parse_sd_jwt_vc"]
