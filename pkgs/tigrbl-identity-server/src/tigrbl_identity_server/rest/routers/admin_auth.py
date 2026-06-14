from __future__ import annotations

from tigrbl_identity_server.framework import AsyncSession, Depends, HTTPException, JSONResponse, RedirectResponse, Request, Response, TigrblRouter, select, status
from tigrbl_identity_contracts.rest import (
    AdminPasswordChangeIn,
    AdminPasswordResetCompleteIn,
    AdminPasswordResetRequestIn,
    AdminSessionOut,
    CredsIn,
)
from tigrbl_identity_server.ops.login import login_user
from tigrbl_identity_admin.bootstrap import (
    consume_password_reset_token,
    issue_password_reset_token,
    resolve_admin_user_from_request,
    user_is_admin,
)
from tigrbl_identity_jose.key_management import hash_pw
from tigrbl_identity_runtime.http_standards.cookies import clear_session_cookie
from tigrbl_identity_oidc.standards.session_mgmt import resolve_browser_session
from tigrbl_identity_storage.tables import User
from tigrbl_identity_storage.tables.engine import get_db

api = router = TigrblRouter()
ADMIN_AUTH_TAGS = ["Admin Auth"]


def _session_payload(user: User | None, *, session_id: str | None = None, debug_reset_token: str | None = None) -> AdminSessionOut:
    return AdminSessionOut(
        authenticated=user is not None,
        session_id=session_id,
        user_id=str(user.id) if user is not None else None,
        tenant_id=str(user.tenant_id) if user is not None else None,
        username=getattr(user, "username", None) if user is not None else None,
        email=getattr(user, "email", None) if user is not None else None,
        is_admin=bool(getattr(user, "is_admin", False)) if user is not None else False,
        is_superuser=bool(getattr(user, "is_superuser", False)) if user is not None else False,
        must_change_password=bool(getattr(user, "must_change_password", False)) if user is not None else False,
        roles=list(getattr(user, "roles", ()) if user is not None else ()),
        debug_reset_token=debug_reset_token,
    )


@api.route("/admin/auth/login", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_login(request: Request, creds: CredsIn | None = None, db: AsyncSession = Depends(get_db)):
    if creds is None:
        body = await request.json() or {}
        creds = CredsIn.model_validate(body)
    row = await db.scalar(select(User).where((User.username == creds.identifier) | (User.email == creds.identifier)))
    if row is None or not user_is_admin(row):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "administrator authorization required")
    login_response = await login_user(request=request, db=db, identifier=creds.identifier, password=creds.password)
    response = JSONResponse(_session_payload(row, session_id=None).model_dump())
    set_cookie = login_response.headers.get("set-cookie")
    if set_cookie:
        response.headers["set-cookie"] = set_cookie
    return response


@api.route("/admin/auth/login", methods=["GET"], tags=ADMIN_AUTH_TAGS)
async def admin_login_browser_redirect() -> Response:
    return RedirectResponse(url="/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@api.route("/admin/auth/session", methods=["GET"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_session(request: Request):
    session_row = await resolve_browser_session(request)
    user = await resolve_admin_user_from_request(request)
    if session_row is None or user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return _session_payload(user, session_id=str(session_row.id))


@api.route("/admin/auth/logout", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_logout() -> Response:
    response = JSONResponse(AdminSessionOut(authenticated=False).model_dump())
    clear_session_cookie(response)
    return response


@api.route("/admin/auth/forgot-password", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_forgot_password(
    request: Request,
    payload: AdminPasswordResetRequestIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    if payload is None:
        body = await request.json() or {}
        payload = AdminPasswordResetRequestIn.model_validate(body)
    row = await db.scalar(select(User).where((User.username == payload.identifier) | (User.email == payload.identifier)))
    debug_token = None
    if row is not None and user_is_admin(row):
        debug_token = await issue_password_reset_token(user=row)
        from tigrbl_identity_runtime.settings import settings

        if not settings.admin_password_reset_debug_disclosure:
            debug_token = None
    return _session_payload(None, debug_reset_token=debug_token)


@api.route("/admin/auth/reset-password", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_reset_password(request: Request, payload: AdminPasswordResetCompleteIn | None = None):
    if payload is None:
        body = await request.json() or {}
        payload = AdminPasswordResetCompleteIn.model_validate(body)
    user = await consume_password_reset_token(token=payload.token, new_password=payload.password)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid or expired reset token")
    response = JSONResponse(_session_payload(None).model_dump())
    clear_session_cookie(response)
    return response


@api.route("/admin/auth/change-password", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_change_password(
    request: Request,
    payload: AdminPasswordChangeIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    if payload is None:
        body = await request.json() or {}
        payload = AdminPasswordChangeIn.model_validate(body)
    user = await resolve_admin_user_from_request(request)
    session_row = await resolve_browser_session(request)
    if user is None or session_row is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    if not user.verify_password(payload.current_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid current password")
    row = await db.scalar(select(User).where(User.id == user.id))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    row.password_hash = hash_pw(payload.new_password)
    row.must_change_password = False
    row.password_reset_token_hash = None
    row.password_reset_expires_at = None
    await db.commit()
    return _session_payload(row, session_id=str(session_row.id))


__all__ = ["router", "api"]
