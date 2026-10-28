"""RFC 8615 well-known endpoint metadata for the release path."""

from __future__ import annotations

RFC8615_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc8615"
WELL_KNOWN_PREFIX = "/.well-known"
WELL_KNOWN_ENDPOINTS = {
    "openid_configuration": f"{WELL_KNOWN_PREFIX}/openid-configuration",
    "oauth_authorization_server": f"{WELL_KNOWN_PREFIX}/oauth-authorization-server",
    "oauth_protected_resource": f"{WELL_KNOWN_PREFIX}/oauth-protected-resource",
    "jwks": f"{WELL_KNOWN_PREFIX}/jwks.json",
}

__all__ = ["RFC8615_SPEC_URL", "WELL_KNOWN_PREFIX", "WELL_KNOWN_ENDPOINTS"]
