"""Compatibility facade for canonical RFC 9207 issuer-identification helpers."""

from tigrbl_auth.standards.oauth2.issuer_identification import (
    RFC9207_SPEC_URL,
    OWNER,
    STATUS,
    StandardOwner,
    describe,
    extract_issuer,
)

__all__ = ["STATUS", "RFC9207_SPEC_URL", "StandardOwner", "OWNER", "extract_issuer", "describe"]
