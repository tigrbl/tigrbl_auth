from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from tigrbl_auth.framework import HTTPException, JSONResponse, select, status
from tigrbl_auth.api.rest.shared import _jwt, _require_tls
from tigrbl_auth.config.settings import settings
from tigrbl_auth.services.persistence import append_audit_event_async
from tigrbl_auth.services.token_service import issue_persisted_token_pair
from tigrbl_auth.standards.http.cookies import issue_session_cookie, session_cookie_policy
from tigrbl_auth.oidc_id_token import mint_id_token
from tigrbl_auth.standards.oidc.session_mgmt import create_browser_session
from tigrbl_auth.standards.oauth2.rfc8414_metadata import ISSUER
from tigrbl_auth.tables import User


async def login_user(*, request, db, identifier: str, password: str) -> JSONResponse:
    _require_tls(request)
    row = await db.scalar(select(User).where(User.username == identifier))
    if row is None:
        row = await db.scalar(select(User).where(User.email == identifier))
    if row is None or not row.verify_password(password):
        raise HTTPException(status_code=400, detail="invalid credentials")

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=max(int(session_cookie_policy().max_age_seconds), 60))
    session_row, cookie_secret = await create_browser_session(
        user_id=row.id,
        tenant_id=row.tenant_id,
        username=row.username,
        expires_at=expires_at,
    )
    access, refresh = await issue_persisted_token_pair(
        jwt=_jwt,
        sub=str(session_row.user_id),
        tid=str(session_row.tenant_id),
        client_id=None,
        scope="openid profile email",
        issuer=ISSUER,
        audience=settings.protected_resource_identifier,
    )
    id_token = await mint_id_token(
        sub=str(session_row.user_id),
        aud=ISSUER,
        nonce=secrets.token_urlsafe(8),
        issuer=ISSUER,
        sid=str(session_row.id),
        auth_time=int((session_row.auth_time or datetime.now(timezone.utc)).timestamp()),
    )
    response = JSONResponse({
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "id_token": id_token,
        "session_id": str(session_row.id),
        "cookie_policy": {
            "name": session_cookie_policy().name,
            "same_site": session_cookie_policy().same_site,
            "secure": session_cookie_policy().secure,
        },
    })
    issue_session_cookie(response, session_id=session_row.id, secret=cookie_secret, expires_at=session_row.expires_at)
    await append_audit_event_async(
        tenant_id=session_row.tenant_id,
        actor_user_id=session_row.user_id,
        session_id=session_row.id,
        event_type='session.login',
        target_type='session',
        target_id=str(session_row.id),
        details={'identifier': identifier},
    )
    return response
