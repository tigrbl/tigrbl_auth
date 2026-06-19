"""Compatibility facade for canonical RFC 9396 RAR helpers."""

from tigrbl_auth_protocol_oauth.standards.rar import (
    AuthorizationDetail,
    OWNER,
    RFC9396_SPEC_URL,
    STATUS,
    StandardOwner,
    describe,
    parse_authorization_details,
)

__all__ = [
    "STATUS",
    "RFC9396_SPEC_URL",
    "StandardOwner",
    "OWNER",
    "AuthorizationDetail",
    "parse_authorization_details",
    "describe",
]
