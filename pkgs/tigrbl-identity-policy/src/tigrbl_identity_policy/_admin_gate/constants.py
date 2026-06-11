from __future__ import annotations

import logging
from typing import Any

from tigrbl.security import APIKey, HTTPBearer, Security

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
ADMIN_OPENAPI_SECURITY_DEPENDENCIES = (
    Security(
        APIKey(
            scheme_name=ADMIN_HEADER_SCHEME,
            name="X-API-Key",
            auto_error=False,
        )
    ),
    Security(
        HTTPBearer(
            scheme_name=ADMIN_BEARER_SCHEME,
            auto_error=False,
        )
    ),
)
logger = logging.getLogger(__name__)
