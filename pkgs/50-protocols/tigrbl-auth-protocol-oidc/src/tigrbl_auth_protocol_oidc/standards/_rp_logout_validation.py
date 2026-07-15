"""OpenID Connect RP-Initiated Logout with durable fanout planning and replay protection."""

from __future__ import annotations

import base64
import json
from typing import Any, Final
from tigrbl_identity_core.standards import StandardOwner
from urllib.parse import urlparse
from uuid import UUID

try:  # dependency-light import path for checkpoint evidence generation
    from http import HTTPStatus as status
    from tigrbl.runtime.status import HTTPException
except Exception:  # pragma: no cover - exercised in dependency-light tests

    class _FallbackStatus:
        HTTP_400_BAD_REQUEST = 400
        HTTP_401_UNAUTHORIZED = 401
        HTTP_404_NOT_FOUND = 404

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    status = _FallbackStatus()

STATUS: Final[str] = "rp-initiated-logout-runtime"


OWNER = StandardOwner(
    label="OIDC RP-Initiated Logout",
    title="OpenID Connect RP-Initiated Logout",
    runtime_status=STATUS,
    public_surface=("/logout",),
    notes=(
        "The canonical /logout route validates registered post-logout redirect URIs, validates id_token_hint "
        "claims against issuer/audience/session policy, persists logout fanout plans, and reuses an existing "
        "logout_state record to provide replay-safe idempotence when logout is retried."
    ),
)


async def _verify_id_token_hint(token: str, *, issuer: str, audience: str):
    from tigrbl_auth_protocol_oidc.standards.id_token import verify_id_token

    return await verify_id_token(token, issuer=issuer, audience=audience)


def _normalized_uris(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str):
        return [item for item in value.split() if item]
    return [str(value)]


def _normalize_uuid(value: Any) -> UUID | None:
    if value in {None, "", False}:
        return None
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return None


def _audiences(claims: dict[str, Any] | None) -> list[str]:
    if not claims:
        return []
    aud = claims.get("aud")
    if aud is None:
        return []
    if isinstance(aud, (list, tuple, set)):
        return [str(item) for item in aud if item not in {None, ""}]
    return [str(aud)] if aud not in {None, ""} else []


def _unsafe_decode_jwt_claims(token: str) -> dict[str, Any]:
    try:
        parts = str(token).split(".")
        if len(parts) != 3:
            return {}
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        return dict(json.loads(base64.urlsafe_b64decode(padded).decode("utf-8")))
    except Exception:
        return {}


def _require_https_if_present(uri: str) -> None:
    parsed = urlparse(uri)
    if parsed.scheme != "https":
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "post_logout_redirect_uri must use https"
        )


def assert_logout_session_active(session_row) -> None:
    if session_row is None:
        return None
    state = str(getattr(session_row, "session_state", "active") or "active").lower()
    if getattr(session_row, "ended_at", None) is not None or state in {
        "terminated",
        "expired",
        "ended",
        "revoked",
    }:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "expired_session"})
