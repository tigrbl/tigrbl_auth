"""Authorization server issuer identification owner and helper module."""

from __future__ import annotations

from typing import Final, Mapping, Sequence

from tigrbl_identity_core.standards import StandardOwner, describe_owner
from urllib.parse import parse_qs, urlparse

from tigrbl_identity_contracts.protocol_configuration import (
    protocol_settings as settings,
)

STATUS: Final[str] = "authorization-response-issuer-runtime"
RFC9207_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9207"


OWNER = StandardOwner(
    label="RFC 9207",
    title="OAuth 2.0 Authorization Server Issuer Identification",
    runtime_status=STATUS,
    public_surface=("/authorize", "/.well-known/openid-configuration"),
    notes=(
        "Canonical standards-tree owner module for issuer parameter emission, redirect-response "
        "parsing, and mix-up resistant validation of authorization-response issuer identifiers."
    ),
)


class IssuerIdentificationError(ValueError):
    """Raised when an authorization response issuer parameter is invalid."""


def _validate_issuer_identifier(value: str) -> str:
    issuer = str(value or "").strip()
    parsed = urlparse(issuer)
    if (
        not issuer
        or parsed.scheme != "https"
        or not parsed.netloc
        or parsed.query
        or parsed.fragment
    ):
        raise IssuerIdentificationError(
            f"invalid issuer identifier: {RFC9207_SPEC_URL}"
        )
    return issuer.rstrip("/") if issuer.endswith("/") else issuer


def _coerce_issuer_values(value: object) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return [str(item) for item in value if str(item)]
    return [str(value)]


def extract_issuer(params: Mapping[str, object], expected_issuer: str) -> str:
    if not settings.enable_rfc9207:
        raise NotImplementedError(
            f"issuer identification not enabled: {RFC9207_SPEC_URL}"
        )
    expected = _validate_issuer_identifier(expected_issuer)
    values = _coerce_issuer_values(params.get("iss"))
    if not values:
        raise IssuerIdentificationError(f"missing iss parameter: {RFC9207_SPEC_URL}")
    normalized = [_validate_issuer_identifier(item) for item in values]
    if len(set(normalized)) != 1:
        raise IssuerIdentificationError(
            f"multiple mismatched issuer identifiers in authorization response: {RFC9207_SPEC_URL}"
        )
    issuer = normalized[0]
    if issuer != expected:
        raise IssuerIdentificationError(f"issuer mismatch: {RFC9207_SPEC_URL}")
    return issuer


def authorization_response_issuer(issuer: str | None = None) -> tuple[str, str]:
    if not settings.enable_rfc9207:
        raise NotImplementedError(
            f"issuer identification not enabled: {RFC9207_SPEC_URL}"
        )
    effective = issuer or settings.issuer
    return ("iss", _validate_issuer_identifier(str(effective)))


def extract_issuer_from_redirect_uri(redirect_uri: str, expected_issuer: str) -> str:
    parsed = urlparse(str(redirect_uri))
    candidates: dict[str, object] = {}
    query_map = {
        key: values
        for key, values in parse_qs(parsed.query, keep_blank_values=True).items()
    }
    fragment_map = {
        key: values
        for key, values in parse_qs(parsed.fragment, keep_blank_values=True).items()
    }
    if "iss" in query_map:
        candidates["iss"] = query_map["iss"]
    elif "iss" in fragment_map:
        candidates["iss"] = fragment_map["iss"]
    return extract_issuer(candidates, expected_issuer)


def issuer_metadata(issuer: str | None = None) -> dict[str, object]:
    return {
        "authorization_response_iss_parameter_supported": bool(settings.enable_rfc9207),
        "issuer": _validate_issuer_identifier(str(issuer or settings.issuer)),
    }


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC9207_SPEC_URL,
    )


__all__ = [
    "STATUS",
    "RFC9207_SPEC_URL",
    "StandardOwner",
    "IssuerIdentificationError",
    "OWNER",
    "extract_issuer",
    "authorization_response_issuer",
    "extract_issuer_from_redirect_uri",
    "issuer_metadata",
    "describe",
]
