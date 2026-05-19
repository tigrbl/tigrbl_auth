"""Compatibility facade for canonical RFC 7592 owner metadata."""

from tigrbl_auth.standards.oauth2.client_registration_management import (
    RFC7592_SPEC_URL,
    OWNER,
    STATUS,
    StandardOwner,
    describe,
)

__all__ = ["STATUS", "RFC7592_SPEC_URL", "StandardOwner", "OWNER", "describe"]
