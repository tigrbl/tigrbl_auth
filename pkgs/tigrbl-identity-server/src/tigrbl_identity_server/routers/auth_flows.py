from __future__ import annotations


import secrets

from tigrbl.security import Depends as TigrblDepends
from tigrbl_identity_server.framework import AsyncSession, HTTPException, JSONResponse, Request
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage.tables import AuthSession, User
from ..routers.schemas import CredsIn, TokenPair
from tigrbl_auth_protocol_oauth.standards.rfc8414_metadata import ISSUER
from tigrbl_auth_protocol_oidc.standards.id_token import mint_id_token
from ..routers.shared import _jwt, _require_tls
from tigrbl_authn_credentials.token_service import issue_persisted_token_pair
from .authz import router as router

api = router


@router.route("/login", methods=["POST"], response_model=TokenPair)
async def login(
    request: Request,
    creds: CredsIn | None = None,
    db: AsyncSession = TigrblDepends(get_db),
):
    _require_tls(request)
    if creds is None:
        body = await request.json() or {}
        creds = CredsIn.model_validate(body)
    users = await User.handlers.list.core(
        {"payload": {"filters": {"username": creds.identifier}}, "db": db}
    )
    user = users[0] if users else None
    if user is None or not user.verify_password(creds.password):
        raise HTTPException(status_code=400, detail="invalid credentials")
    payload = {
        "user_id": user.id,
        "tenant_id": user.tenant_id,
        "username": user.username,
    }
    session = await AuthSession.handlers.create.core({"payload": payload, "db": db})
    await db.commit()
    access, refresh = await issue_persisted_token_pair(
        jwt=_jwt,
        sub=str(session.user_id),
        tid=str(session.tenant_id),
        client_id=None,
        scope="openid profile email",
    )
    id_token = await mint_id_token(
        sub=str(session.user_id),
        aud=ISSUER,
        nonce=secrets.token_urlsafe(8),
        issuer=ISSUER,
        sid=str(session.id),
    )
    pair = {
        "access_token": access,
        "refresh_token": refresh,
        "id_token": id_token,
    }
    response = JSONResponse(pair)
    response.set_cookie("sid", str(session.id), httponly=True, samesite="lax")
    return response


__all__ = ["router", "api"]
