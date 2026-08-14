from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from tigrbl import JSONResponse, Request
from tigrbl.runtime.status import HTTPException
from .security.password_authentication import password_authentication


async def login_user(*, request: Request, db: Any, identifier: str, password: str) -> Any:
    from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER
    from tigrbl_auth_protocol_oidc.id_token import mint_id_token
    from tigrbl_identity_jose.jwt_coder import JWTCoder
    from tigrbl_identity_runtime.http_standards.cookies import issue_session_cookie, session_cookie_policy
    from tigrbl_identity_runtime.settings import settings
    from tigrbl_identity_storage_runtime.revocation import is_revoked_async
    from tigrbl_identity_server.rest.shared import _require_tls
    from tigrbl_identity_server.security.handler_records import (
        append_audit_event_record,
        create_browser_session_record,
        issue_token_pair_records,
    )

    _require_tls(request)
    authentication = await password_authentication.authenticate_password(
        identifier=identifier,
        password=password,
        db=db,
    )
    row = authentication.record
    if not authentication.authenticated or row is None:
        raise HTTPException(status_code=400, detail="invalid credentials")

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=max(int(session_cookie_policy().max_age_seconds), 60))
    session_row, cookie_secret = await create_browser_session_record(
        db,
        user_id=row.id,
        tenant_id=row.tenant_id,
        username=row.username,
        expires_at=expires_at,
    )
    if bool(getattr(row, "must_change_password", False)):
        response = JSONResponse(
            {
                "error": "password_change_required",
                "must_change_password": True,
            },
            status_code=428,
        )
        issue_session_cookie(
            response,
            session_id=session_row.id,
            secret=cookie_secret,
            expires_at=session_row.expires_at,
        )
        await append_audit_event_record(
            db,
            tenant_id=session_row.tenant_id,
            actor_user_id=session_row.user_id,
            session_id=session_row.id,
            event_type="session.password_change_required",
            target_type="session",
            target_id=str(session_row.id),
            details={"identifier": identifier},
        )
        commit = getattr(db, "commit", None)
        if callable(commit):
            result = commit()
            if hasattr(result, "__await__"):
                await result
        return response
    jwt = await JWTCoder.async_default(
        revocation_checker=is_revoked_async,
    )
    access, refresh = await issue_token_pair_records(
        db,
        jwt=jwt,
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
    response = JSONResponse(
        {
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
        }
    )
    issue_session_cookie(response, session_id=session_row.id, secret=cookie_secret, expires_at=session_row.expires_at)
    await append_audit_event_record(
        db,
        tenant_id=session_row.tenant_id,
        actor_user_id=session_row.user_id,
        session_id=session_row.id,
        event_type="session.login",
        target_type="session",
        target_id=str(session_row.id),
        details={"identifier": identifier},
    )
    commit = getattr(db, "commit", None)
    if callable(commit):
        result = commit()
        if hasattr(result, "__await__"):
            await result
    return response


async def change_required_password(
    *,
    request: Request,
    db: Any,
    current_password: str,
    new_password: str,
) -> Any:
    from tigrbl_identity_runtime.deployment import deployment_from_request
    from tigrbl_identity_runtime.http_standards.cookies import clear_session_cookie
    from tigrbl_identity_runtime.settings import settings
    from tigrbl_identity_server.rest.shared import _require_tls
    from tigrbl_identity_server.security.handler_records import (
        append_audit_event_record,
        read_handler_record,
        resolve_browser_session_record,
        update_handler_record,
    )
    from tigrbl_identity_storage.tables import User
    from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher

    deployment = deployment_from_request(request, settings)
    _require_tls(request, deployment=deployment)
    session_row = await resolve_browser_session_record(
        db,
        request,
        deployment=deployment,
    )
    if session_row is None:
        raise HTTPException(status_code=401, detail="password change session required")
    user = await read_handler_record(User, db, session_row.user_id)
    if user is None or not bool(getattr(user, "is_active", True)):
        raise HTTPException(status_code=401, detail="password change session required")
    if not bool(getattr(user, "must_change_password", False)):
        raise HTTPException(status_code=409, detail="password change is not required")

    hasher = BcryptSecretHasher()
    verification = hasher.verify_secret(current_password, user.password_hash)
    if not verification.verified:
        raise HTTPException(status_code=400, detail="invalid current password")
    if current_password == new_password:
        raise HTTPException(
            status_code=400,
            detail="new password must differ from the temporary password",
        )

    user = await update_handler_record(
        User,
        db,
        user.id,
        {
            "password_hash": hasher.hash_secret(new_password).encoded,
            "must_change_password": False,
            "password_reset_token_hash": None,
            "password_reset_expires_at": None,
        },
    )
    await append_audit_event_record(
        db,
        tenant_id=session_row.tenant_id,
        actor_user_id=session_row.user_id,
        session_id=session_row.id,
        event_type="identity.required_password_changed",
        target_type="user",
        target_id=str(user.id),
        details={},
    )
    commit = getattr(db, "commit", None)
    if callable(commit):
        result = commit()
        if hasattr(result, "__await__"):
            await result
    response = JSONResponse({"password_changed": True})
    clear_session_cookie(response)
    return response


__all__ = ["change_required_password", "login_user", "password_authentication"]
