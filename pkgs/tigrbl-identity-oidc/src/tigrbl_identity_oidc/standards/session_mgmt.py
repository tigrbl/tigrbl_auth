from __future__ import annotations

"""OpenID Connect Session Management with durable browser-session handling.

This module deliberately keeps the session-management claim boundary truthful:
- durable browser sessions are persisted server-side
- ``session_state`` values are emitted and can be validated against client origins
- auth-code issuance is bound to the durable browser session
- cookie rotation / renewal / invalidation semantics are repository-owned
- a dedicated mounted ``check_session_iframe`` route is *not* currently claimed
  by discovery or contracts in this checkpoint
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Final
from urllib.parse import urlparse
from uuid import UUID

from tigrbl_identity_runtime.deployment import deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_runtime.http_standards.cookies import (
    extract_session_cookie,
    hash_cookie_secret,
    new_session_cookie_secret,
    new_session_state_salt,
    parse_session_cookie_value,
)

STATUS: Final[str] = "browser-session-runtime"


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


@dataclass(frozen=True, slots=True)
class SessionStateValidation:
    valid: bool
    reason: str
    origin: str
    presented_session_state: str | None
    expected_session_state: str | None


OWNER = StandardOwner(
    label="OIDC Session Management",
    title="OpenID Connect Session Management",
    runtime_status=STATUS,
    public_surface=("/login", "/authorize", "/logout"),
    notes=(
        "Durable browser sessions own opaque session-cookie secrets, cookie rotation, "
        "client binding, auth-code linkage, and OIDC session_state generation + validation across "
        "client origins. This release path does not claim a mounted check_session_iframe endpoint, "
        "and discovery/contracts remain truthful about that omission."
    ),
)


def _persistence():
    from tigrbl_identity_storage import persistence as persistence_module

    return persistence_module


def _utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def _origin(uri: str | None) -> str:
    if not uri:
        return ""
    parsed = urlparse(uri)
    host = parsed.hostname or ""
    port = f":{parsed.port}" if parsed.port else ""
    return f"{parsed.scheme}://{host}{port}" if parsed.scheme and host else uri


def session_client_origin(redirect_uri: str | None) -> str:
    return _origin(redirect_uri)


def compute_session_state(*, client_id: str, redirect_uri: str, session_id: UUID | str, salt: str, issuer: str | None = None) -> str:
    origin = _origin(redirect_uri)
    payload = f"{client_id} {origin} {session_id} {salt} {issuer or settings.issuer}"
    return f"{sha256(payload.encode('utf-8')).hexdigest()}.{salt}"


def parse_session_state(value: str | None) -> tuple[str, str] | None:
    if not value or not isinstance(value, str):
        return None
    if "." not in value:
        return None
    digest, salt = value.rsplit(".", 1)
    if len(digest) != 64 or not salt:
        return None
    try:
        int(digest, 16)
    except Exception:
        return None
    return digest, salt


def validate_session_state(
    *,
    presented_session_state: str | None,
    client_id: str,
    redirect_uri: str,
    session_id: UUID | str,
    salt: str | None = None,
    expected_session_state: str | None = None,
    issuer: str | None = None,
) -> SessionStateValidation:
    origin = _origin(redirect_uri)
    parsed_presented = parse_session_state(presented_session_state)
    if parsed_presented is None:
        return SessionStateValidation(
            valid=False,
            reason="malformed_session_state",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=expected_session_state,
        )
    presented_digest, presented_salt = parsed_presented
    effective_salt = salt or presented_salt
    effective_expected = expected_session_state or compute_session_state(
        client_id=client_id,
        redirect_uri=redirect_uri,
        session_id=session_id,
        salt=effective_salt,
        issuer=issuer,
    )
    parsed_expected = parse_session_state(effective_expected)
    if parsed_expected is None:
        return SessionStateValidation(
            valid=False,
            reason="invalid_expected_session_state",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=effective_expected,
        )
    expected_digest, expected_salt = parsed_expected
    if presented_salt != expected_salt:
        return SessionStateValidation(
            valid=False,
            reason="salt_mismatch",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=effective_expected,
        )
    if presented_digest != expected_digest:
        return SessionStateValidation(
            valid=False,
            reason="hash_mismatch",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=effective_expected,
        )
    return SessionStateValidation(
        valid=True,
        reason="validated",
        origin=origin,
        presented_session_state=presented_session_state,
        expected_session_state=effective_expected,
    )


async def create_browser_session(*, user_id: UUID, tenant_id: UUID, username: str, client_id: UUID | None = None, expires_at: datetime | None = None):
    persistence = _persistence()
    secret = new_session_cookie_secret()
    salt = new_session_state_salt()
    row = await persistence.create_session_async(
        user_id=user_id,
        tenant_id=tenant_id,
        username=username,
        client_id=client_id,
        expires_at=expires_at,
        cookie_secret_hash=hash_cookie_secret(secret),
        session_state_salt=salt,
    )
    return row, secret


async def resolve_browser_session(request, *, deployment=None):
    deployment = deployment if deployment is not None else deployment_from_request(request, settings)
    if not deployment.flag_enabled("enable_oidc_session_management"):
        return None
    parsed = parse_session_cookie_value(extract_session_cookie(request))
    if parsed is None:
        return None
    persistence = _persistence()
    row = await persistence.get_active_session_async(parsed.session_id)
    if row is None:
        return None
    if parsed.secret:
        if not row.cookie_secret_hash or row.cookie_secret_hash != hash_cookie_secret(parsed.secret):
            return None
    await persistence.touch_session_async(row.id)
    return row


async def bind_browser_session_client(session_id: UUID, *, client_id: UUID | None):
    return await _persistence().bind_session_client_async(session_id, client_id=client_id)


async def maybe_rotate_browser_session_cookie(session_row):
    if session_row is None:
        return None
    renewal_seconds = max(int(settings.session_cookie_renewal_seconds), 60)
    now = datetime.now(timezone.utc)
    rotated_at = _utc(getattr(session_row, 'cookie_rotated_at', None)) or _utc(getattr(session_row, 'cookie_issued_at', None))
    if rotated_at is None or (now - rotated_at).total_seconds() >= renewal_seconds:
        secret = new_session_cookie_secret()
        await _persistence().rotate_session_cookie_secret_async(session_row.id, cookie_secret_hash=hash_cookie_secret(secret))
        return secret
    return None


def session_state_for_client(session_row, *, client_id: str, redirect_uri: str, deployment=None, issuer: str | None = None) -> str | None:
    if session_row is None:
        return None
    deployment = deployment if deployment is not None else resolve_deployment(settings)
    if not deployment.flag_enabled("enable_oidc_session_management"):
        return None
    salt = getattr(session_row, 'session_state_salt', None) or new_session_state_salt()
    return compute_session_state(
        client_id=client_id,
        redirect_uri=redirect_uri,
        session_id=session_row.id,
        salt=salt,
        issuer=issuer or getattr(deployment, "issuer", None),
    )


def validate_session_state_for_client(
    session_row,
    *,
    presented_session_state: str | None,
    client_id: str,
    redirect_uri: str,
    deployment=None,
    issuer: str | None = None,
) -> SessionStateValidation:
    if session_row is None:
        return SessionStateValidation(
            valid=False,
            reason="no_session",
            origin=_origin(redirect_uri),
            presented_session_state=presented_session_state,
            expected_session_state=None,
        )
    return validate_session_state(
        presented_session_state=presented_session_state,
        client_id=client_id,
        redirect_uri=redirect_uri,
        session_id=session_row.id,
        salt=getattr(session_row, 'session_state_salt', None),
        issuer=issuer or getattr(deployment, "issuer", None),
    )


async def touch_browser_session(session_id: UUID):
    return await _persistence().touch_session_async(session_id)


async def terminate_browser_session(session_id: UUID, **kwargs):
    return await _persistence().terminate_session_async(session_id, **kwargs)


def describe(*, request=None, deployment=None) -> dict[str, object]:
    if deployment is None:
        deployment = deployment_from_request(request, settings) if request is not None else resolve_deployment(settings)
    return {
        "label": OWNER.label,
        "title": OWNER.title,
        "runtime_status": OWNER.runtime_status,
        "public_surface": list(OWNER.public_surface),
        "cookie_name": settings.session_cookie_name,
        "cookie_rotation_seconds": int(settings.session_cookie_renewal_seconds),
        "same_site_default": settings.session_cookie_samesite,
        "session_state_validation_supported": True,
        "session_state_origin_bound": True,
        "auth_code_linkage_supported": True,
        "check_session_iframe_claimed": False,
        "cross_site_logout_enabled": deployment.flag_enabled("enable_oidc_frontchannel_logout"),
        "notes": OWNER.notes,
    }


__all__ = [
    "STATUS",
    "SessionStateValidation",
    "StandardOwner",
    "OWNER",
    "bind_browser_session_client",
    "compute_session_state",
    "create_browser_session",
    "describe",
    "maybe_rotate_browser_session_cookie",
    "parse_session_state",
    "resolve_browser_session",
    "session_client_origin",
    "session_state_for_client",
    "terminate_browser_session",
    "touch_browser_session",
    "validate_session_state",
    "validate_session_state_for_client",
]
