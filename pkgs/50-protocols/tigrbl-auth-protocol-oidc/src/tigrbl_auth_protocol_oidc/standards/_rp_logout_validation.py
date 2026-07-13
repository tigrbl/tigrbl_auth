"""OpenID Connect RP-Initiated Logout with durable fanout planning and replay protection."""

from __future__ import annotations

from datetime import datetime, timezone
import base64
import json
from types import SimpleNamespace
from typing import Any, Final
from tigrbl_identity_contracts.oidc import LogoutRequestContext
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from urllib.parse import urlparse
from uuid import UUID

from tigrbl_identity_runtime.deployment import (
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_identity_runtime.settings import settings

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


def _persistence():
    from tigrbl_identity_storage.persistence import get_active_session_async
    from tigrbl_identity_storage.tables.auth_session import AuthSession
    from tigrbl_identity_storage.tables.client_registration import ClientRegistration
    from tigrbl_identity_storage.tables.engine import storage_session
    from tigrbl_identity_storage.tables.logout_state import LogoutState

    async def get_client_registration_async(client_id):
        async with storage_session() as db:
            result = await ClientRegistration.handlers.list.core(
                {"payload": {"filters": {"client_id": client_id}}, "db": db}
            )
        if isinstance(result, dict) and isinstance(result.get("items"), list):
            rows = result["items"]
        else:
            rows = result if isinstance(result, list) else []
        return rows[0] if rows else None

    async def get_latest_logout_for_session_async(session_id):
        async with storage_session() as db:
            return await LogoutState.handlers.latest_for_session.core(
                {"payload": {"session_id": session_id}, "db": db}
            )

    async def terminate_session_async(session_id, **kwargs):
        async with storage_session() as db:
            session = await AuthSession.handlers.terminate.core(
                {"path_params": {"id": session_id}, "payload": kwargs, "db": db}
            )
            if session is None:
                return None
            return await LogoutState.handlers.ensure_for_session.core(
                {"payload": {"session_id": session_id, **kwargs}, "db": db}
            )

    async def update_logout_metadata_async(logout_id, **kwargs):
        async with storage_session() as db:
            return await LogoutState.handlers.update_metadata.core(
                {
                    "path_params": {"id": logout_id},
                    "payload": {"logout_id": logout_id, **kwargs},
                    "db": db,
                }
            )

    return SimpleNamespace(
        get_active_session_async=get_active_session_async,
        get_client_registration_async=get_client_registration_async,
        get_latest_logout_for_session_async=get_latest_logout_for_session_async,
        terminate_session_async=terminate_session_async,
        update_logout_metadata_async=update_logout_metadata_async,
    )


def _frontchannel_builder():
    from tigrbl_auth_protocol_oidc.standards.frontchannel_logout import (
        build_frontchannel_descriptor,
    )

    return build_frontchannel_descriptor


def _backchannel_builder():
    from tigrbl_auth_protocol_oidc.standards.backchannel_logout import (
        build_backchannel_descriptor,
    )

    return build_backchannel_descriptor


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


