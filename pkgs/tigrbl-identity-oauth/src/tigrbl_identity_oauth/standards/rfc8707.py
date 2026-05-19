"""Compatibility facade for canonical RFC 8707 resource-indicator helpers."""

from tigrbl_auth.standards.oauth2.resource_indicators import (
    RFC8707_SPEC_URL,
    OWNER,
    STATUS,
    StandardOwner,
    describe,
    extract_resource,
)

__all__ = ["STATUS", "RFC8707_SPEC_URL", "StandardOwner", "OWNER", "extract_resource", "describe"]
