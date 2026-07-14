"""Runtime OAuth token revocation publisher backed by identity storage."""

from __future__ import annotations

from urllib.parse import parse_qs

from tigrbl_auth_protocol_oauth.schemas import RevocationOut
from tigrbl_identity_runtime.settings import settings
from tigrbl import (
    Request,
    TigrblApp,
    TigrblRouter,
)
from tigrbl.runtime.status import HTTPException, status
from .token_lifecycle import (
    is_revoked,
    is_revoked_async,
    is_token_revoked,
    is_token_revoked_async,
    reset_revocations,
    reset_revocations_async,
    reset_token_state,
    reset_token_state_async,
    revoke_token,
    revoke_token_async,
)
from .ops.audit import append_audit_event_async

RFC7009_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc7009"
CANONICAL_REVOCATION_PATH = "/revoke"

api = router = TigrblRouter()


@api.route(CANONICAL_REVOCATION_PATH, methods=["POST"], response_model=RevocationOut)
async def revoke(request: Request) -> dict[str, bool]:
    if not settings.enable_rfc7009:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"RFC 7009 disabled: {RFC7009_SPEC_URL}"
        )
    body = getattr(request, "body", b"") or b""
    form_data = parse_qs(body.decode("utf-8"), keep_blank_values=True)
    token = (form_data.get("token") or [None])[0]
    token_type_hint = (form_data.get("token_type_hint") or [None])[0]
    if not token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "token parameter required")

    await revoke_token_async(
        token, token_type_hint=token_type_hint, reason="revoked_via_endpoint"
    )
    await append_audit_event_async(
        event_type="token.revoked",
        target_type="token",
        target_id=token[:16],
        details={"token_type_hint": token_type_hint},
    )
    return {"revoked": True}


def include_revocation_endpoint(app: TigrblApp) -> None:
    if settings.enable_rfc7009 and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == CANONICAL_REVOCATION_PATH
        for route in app.router.routes
    ):
        app.include_router(api)


include_rfc7009 = include_revocation_endpoint


__all__ = [
    "CANONICAL_REVOCATION_PATH",
    "RFC7009_SPEC_URL",
    "api",
    "router",
    "revoke",
    "revoke_token",
    "revoke_token_async",
    "is_revoked",
    "is_revoked_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "reset_revocations",
    "reset_revocations_async",
    "reset_token_state",
    "reset_token_state_async",
    "include_revocation_endpoint",
    "include_rfc7009",
]
