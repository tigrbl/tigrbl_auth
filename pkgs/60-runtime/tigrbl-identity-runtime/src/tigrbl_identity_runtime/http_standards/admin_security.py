"""Shared administrative HTTP security names and OpenAPI declarations."""

from typing import Any

ADMIN_API_KEY_ENV = "TIGRBL_AUTH_ADMIN_API_KEY"
ADMIN_API_KEY_HEADER = "x-api-key"
ADMIN_BEARER_SCHEME = "AdminBearer"
ADMIN_HEADER_SCHEME = "AdminApiKeyHeader"
ADMIN_SECURITY_SCHEMES: dict[str, dict[str, Any]] = {
    ADMIN_HEADER_SCHEME: {"type": "apiKey", "in": "header", "name": "X-API-Key"},
    ADMIN_BEARER_SCHEME: {"type": "http", "scheme": "bearer"},
}
ADMIN_SECURITY_REQUIREMENT: list[dict[str, list[Any]]] = [
    {ADMIN_HEADER_SCHEME: []},
    {ADMIN_BEARER_SCHEME: []},
]

__all__ = [
    "ADMIN_API_KEY_ENV",
    "ADMIN_API_KEY_HEADER",
    "ADMIN_BEARER_SCHEME",
    "ADMIN_HEADER_SCHEME",
    "ADMIN_SECURITY_REQUIREMENT",
    "ADMIN_SECURITY_SCHEMES",
]
