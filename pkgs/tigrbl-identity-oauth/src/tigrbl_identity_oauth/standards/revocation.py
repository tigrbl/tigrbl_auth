"""Domain-organized OAuth 2.0 token revocation support backed by durable persistence."""

from __future__ import annotations

from typing import Final
from urllib.parse import parse_qs

from tigrbl_auth.config.settings import settings
from tigrbl_auth.framework import HTTPException, Request, TigrblApp, TigrblRouter, status
from tigrbl_auth.services.persistence import (
    is_token_revoked as _is_token_revoked,
    reset_token_state as _reset_token_state,
    revoke_token as _revoke_token,
)

RFC7009_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7009"
CANONICAL_REVOCATION_PATH: Final[str] = "/revoke"
LEGACY_REVOCATION_PATH: Final[str] = "/revoked_tokens/revoke"

api = TigrblRouter()
legacy_api = TigrblRouter()
router = api


def revoke_token(token: str, token_type_hint: str | None = None) -> str | None:
    if not settings.enable_rfc7009:
        return None
    return _revoke_token(token, token_type_hint=token_type_hint)


def is_revoked(token: str) -> bool:
    if not settings.enable_rfc7009:
        return False
    return bool(_is_token_revoked(token))


def reset_revocations() -> None:
    _reset_token_state()


@api.route(CANONICAL_REVOCATION_PATH, methods=["POST"])
async def revoke(request: Request) -> dict[str, str]:
    if not settings.enable_rfc7009:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"RFC 7009 disabled: {RFC7009_SPEC_URL}")
    body = getattr(request, "body", b"") or b""
    parsed = parse_qs(body.decode("utf-8"), keep_blank_values=True)
    token = (parsed.get("token") or [None])[0]
    token_type_hint = (parsed.get("token_type_hint") or [None])[0]
    if token is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "missing token")
    revoke_token(token, token_type_hint=token_type_hint)
    return {}


@legacy_api.route(LEGACY_REVOCATION_PATH, methods=["POST"])
async def revoke_legacy(request: Request) -> dict[str, str]:
    return await revoke(request)


def include_revocation_endpoint(app: TigrblApp, *, include_legacy: bool = False) -> None:
    if settings.enable_rfc7009 and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) == CANONICAL_REVOCATION_PATH
        for route in app.router.routes
    ):
        app.include_router(api)
    if include_legacy and settings.enable_rfc7009 and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) == LEGACY_REVOCATION_PATH
        for route in app.router.routes
    ):
        app.include_router(legacy_api)


def include_legacy_revocation_endpoint(app: TigrblApp) -> None:
    include_revocation_endpoint(app, include_legacy=True)


include_rfc7009 = include_revocation_endpoint


__all__ = [
    "RFC7009_SPEC_URL",
    "CANONICAL_REVOCATION_PATH",
    "LEGACY_REVOCATION_PATH",
    "api",
    "legacy_api",
    "router",
    "revoke_token",
    "is_revoked",
    "reset_revocations",
    "include_revocation_endpoint",
    "include_legacy_revocation_endpoint",
    "include_rfc7009",
]
