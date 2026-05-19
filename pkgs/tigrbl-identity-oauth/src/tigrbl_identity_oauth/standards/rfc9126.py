"""Compatibility facade for canonical RFC 9126 owner metadata."""

from tigrbl_auth.standards.oauth2.par import (
    RFC9126_SPEC_URL,
    OWNER,
    STATUS,
    StandardOwner,
    describe,
)

__all__ = ["STATUS", "RFC9126_SPEC_URL", "StandardOwner", "OWNER", "describe"]
