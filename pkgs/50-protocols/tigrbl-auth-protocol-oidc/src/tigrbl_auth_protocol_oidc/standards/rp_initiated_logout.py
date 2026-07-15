"""OpenID Connect RP-Initiated Logout with durable fanout planning and replay protection."""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Final, Mapping
from tigrbl_identity_contracts.oidc import LogoutRequestContext
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from uuid import UUID

from ._rp_logout_validation import (
    OWNER,
    _audiences,
    _normalize_uuid,
    _normalized_uris,
    _require_https_if_present,
    _unsafe_decode_jwt_claims,
    _verify_id_token_hint,
    assert_logout_session_active,
)

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


async def validate_post_logout_redirect_uri(
    *,
    client_id: UUID | None,
    post_logout_redirect_uri: str | None,
    registration_metadata: Mapping[str, Any] | None,
) -> str | None:
    if not post_logout_redirect_uri:
        return None
    _require_https_if_present(post_logout_redirect_uri)
    if client_id is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_client",
                "error_description": "client_id required when post_logout_redirect_uri is supplied",
            },
        )
    metadata = dict(registration_metadata or {})
    allowed = _normalized_uris(metadata.get("post_logout_redirect_uris"))
    if post_logout_redirect_uri not in allowed:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_request",
                "error_description": "unregistered post_logout_redirect_uri",
            },
        )
    return post_logout_redirect_uri


async def validate_id_token_hint(
    *,
    id_token_hint: str | None,
    client_id: UUID | str | None = None,
    session_id: UUID | str | None = None,
    issuer: str | None = None,
) -> dict[str, Any] | None:
    if not id_token_hint:
        return None
    effective_issuer = str(issuer or "").strip()
    if not effective_issuer:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"error": "invalid_id_token_hint", "error_description": "issuer required"},
        )
    effective_client_id = _normalize_uuid(client_id)
    if effective_client_id is None:
        unverified = _unsafe_decode_jwt_claims(id_token_hint)
        for audience in _audiences(unverified):
            parsed = _normalize_uuid(audience)
            if parsed is not None:
                effective_client_id = parsed
                break
    if effective_client_id is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_id_token_hint",
                "error_description": "unable to derive client_id from id_token_hint",
            },
        )
    try:
        claims = dict(
            await _verify_id_token_hint(
                id_token_hint,
                issuer=effective_issuer,
                audience=str(effective_client_id),
            )
        )
    except Exception as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, {"error": "invalid_id_token_hint"}
        ) from exc
    if str(claims.get("iss") or "") != effective_issuer:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"error": "invalid_id_token_hint", "error_description": "issuer mismatch"},
        )
    audiences = _audiences(claims)
    if str(effective_client_id) not in audiences:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_id_token_hint",
                "error_description": "audience mismatch",
            },
        )
    expected_session_id = _normalize_uuid(session_id)
    if expected_session_id is not None:
        sid = _normalize_uuid(claims.get("sid"))
        if sid is not None and sid != expected_session_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {"error": "invalid_id_token_hint", "error_description": "sid mismatch"},
            )
    return claims


def resolve_logout_client_id(
    *,
    requested_client_id: UUID | str | None,
    session_row=None,
    hint_claims: dict[str, Any] | None = None,
) -> UUID | None:
    requested = _normalize_uuid(requested_client_id)
    session_client = (
        _normalize_uuid(getattr(session_row, "client_id", None))
        if session_row is not None
        else None
    )
    hint_candidates = {
        _normalize_uuid(audience) for audience in _audiences(hint_claims)
    }
    hint_candidates.discard(None)

    if (
        requested is not None
        and session_client is not None
        and requested != session_client
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_client",
                "error_description": "requested client does not own the session",
            },
        )
    if requested is not None and hint_candidates and requested not in hint_candidates:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_client",
                "error_description": "requested client does not match id_token_hint",
            },
        )
    if (
        session_client is not None
        and hint_candidates
        and session_client not in hint_candidates
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_client",
                "error_description": "session client does not match id_token_hint",
            },
        )

    if requested is not None:
        return requested
    if session_client is not None:
        return session_client
    for candidate in hint_candidates:
        return candidate
    return None


async def validate_logout_request(
    *,
    requested_client_id: UUID | str | None,
    post_logout_redirect_uri: str | None,
    id_token_hint: str | None,
    session_row=None,
    issuer: str | None = None,
    registration_resolver: Callable[[UUID], Awaitable[Any]] | None = None,
) -> LogoutRequestContext:
    assert_logout_session_active(session_row)
    prevalidated_client_id = _normalize_uuid(requested_client_id) or _normalize_uuid(
        getattr(session_row, "client_id", None)
    )
    hint_claims = await validate_id_token_hint(
        id_token_hint=id_token_hint,
        client_id=prevalidated_client_id,
        session_id=getattr(session_row, "id", None),
        issuer=issuer,
    )
    client_id = resolve_logout_client_id(
        requested_client_id=requested_client_id,
        session_row=session_row,
        hint_claims=hint_claims,
    )
    registration_metadata: Mapping[str, Any] | None = None
    if post_logout_redirect_uri and client_id is not None:
        if registration_resolver is None:
            raise RuntimeError(
                "logout validation requires an injected registration resolver"
            )
        registration = await registration_resolver(client_id)
        registration_metadata = dict(
            getattr(registration, "registration_metadata", {}) or {}
        )
    redirect_uri = await validate_post_logout_redirect_uri(
        client_id=client_id,
        post_logout_redirect_uri=post_logout_redirect_uri,
        registration_metadata=registration_metadata,
    )
    return LogoutRequestContext(
        client_id=client_id,
        post_logout_redirect_uri=redirect_uri,
        id_token_hint_claims=hint_claims,
    )


def describe(*, deployment=None) -> dict[str, object]:
    return describe_owner(
        OWNER,
        id_token_hint_validation_supported=True,
        post_logout_redirect_uri_validation_supported=True,
        idempotent_replay_protection=True,
        frontchannel_logout_supported=bool(
            getattr(deployment, "flag_enabled", lambda *_: True)(
                "enable_oidc_frontchannel_logout"
            )
        )
        if deployment is not None
        else True,
        backchannel_logout_supported=bool(
            getattr(deployment, "flag_enabled", lambda *_: True)(
                "enable_oidc_backchannel_logout"
            )
        )
        if deployment is not None
        else True,
    )


__all__ = [
    "STATUS",
    "LogoutRequestContext",
    "StandardOwner",
    "OWNER",
    "assert_logout_session_active",
    "describe",
    "resolve_logout_client_id",
    "validate_id_token_hint",
    "validate_logout_request",
    "validate_post_logout_redirect_uri",
]
