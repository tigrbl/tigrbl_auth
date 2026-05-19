from __future__ import annotations

from urllib.parse import parse_qs

from tigrbl_auth.config.settings import settings
from tigrbl_auth.framework import HTTPException, status
from tigrbl_auth.services.persistence import append_audit_event_async, revoke_token_async


async def revoke_request(*, request):
    if not settings.enable_rfc7009:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "revocation disabled")
    body = getattr(request, "body", b"") or b""
    form_data = parse_qs(body.decode("utf-8"), keep_blank_values=True)
    token = (form_data.get("token") or [None])[0]
    token_type_hint = (form_data.get("token_type_hint") or [None])[0]
    if not token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "token parameter required")

    await revoke_token_async(token, token_type_hint=token_type_hint, reason="revoked_via_endpoint")
    await append_audit_event_async(
        event_type="token.revoked",
        target_type="token",
        target_id=token[:16],
        details={"token_type_hint": token_type_hint},
    )
    return {"revoked": True}
