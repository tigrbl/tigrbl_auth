"""Compatibility facade for canonical RFC 7591 owner metadata."""

from tigrbl_auth.standards.oauth2.dynamic_client_registration import (
    RFC7591_SPEC_URL,
    OWNER,
    STATUS,
    StandardOwner,
    describe,
)

__all__ = ["STATUS", "RFC7591_SPEC_URL", "StandardOwner", "OWNER", "describe"]
