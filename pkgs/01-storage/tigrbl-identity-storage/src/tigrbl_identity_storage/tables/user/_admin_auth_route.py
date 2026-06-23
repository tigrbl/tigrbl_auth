"""Admin authentication routes bound to the User storage table."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Depends, HTTPException, JSONResponse, RedirectResponse, Request, Response, status

from ..engine import get_db
from ._table import (
    ADMIN_AUTH_TAGS,
    AdminPasswordChangeIn,
    AdminPasswordResetCompleteIn,
    AdminPasswordResetRequestIn,
    AdminSessionOut,
    CredsIn,
    User,
    admin_api,
)
from .._ops import first_record, read_record, update_record
from tigrbl_identity_jose.key_management import hash_pw


def _admin_session_payload(
    user: User | None,
    *,
    session_id: str | None = None,
    debug_reset_token: str | None = None,
) -> AdminSessionOut:
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


async def _find_user_by_identifier(db: Any, identifier: str) -> User | None:
    row = await first_record(User, db, {"username": identifier})
    if row is not None:
        return row
    return await first_record(User, db, {"email": identifier})


async def _resolve_admin_session_and_user(request: Request, db: Any) -> tuple[Any, User]:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request
    from tigrbl_identity_runtime.deployment import deployment_from_request
    from tigrbl_identity_runtime.settings import settings
    from tigrbl_identity_server.security.handler_records import resolve_browser_session_record

    session_row = await resolve_browser_session_record(
        db,
        request,
        deployment=deployment_from_request(request, settings),
    )
    user = await resolve_admin_user_from_request(request, db=db)
    if session_row is None or user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return session_row, user


@admin_api.route("/admin/auth/login", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_login(request: Request, creds: CredsIn | None = None, db: Any = Depends(get_db)) -> Response:
    from tigrbl_identity_admin.bootstrap import user_is_admin
    from ..auth_session._ops import login_user

    if creds is None:
        creds = CredsIn.model_validate(await request.json() or {})
    row = await _find_user_by_identifier(db, creds.identifier)
    if row is None or not user_is_admin(row):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "administrator authorization required")
    login_response = await login_user(request=request, db=db, identifier=creds.identifier, password=creds.password)
    response = JSONResponse(_admin_session_payload(row, session_id=None).model_dump())
    set_cookie = login_response.headers.get("set-cookie")
    if set_cookie:
        response.headers["set-cookie"] = set_cookie
    return response


@admin_api.route("/admin/auth/login", methods=["GET"], tags=ADMIN_AUTH_TAGS)
async def admin_login_browser_redirect() -> Response:
    return RedirectResponse(url="/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@admin_api.route("/admin/auth/session", methods=["GET"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_session(request: Request, db: Any = Depends(get_db)) -> AdminSessionOut:
    session_row, user = await _resolve_admin_session_and_user(request, db)
    return _admin_session_payload(user, session_id=str(session_row.id))


@admin_api.route("/admin/auth/logout", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_logout() -> Response:
    from tigrbl_identity_runtime.http_standards.cookies import clear_session_cookie

    response = JSONResponse(AdminSessionOut(authenticated=False).model_dump())
    clear_session_cookie(response)
    return response


@admin_api.route("/admin/auth/forgot-password", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_forgot_password(
    request: Request,
    payload: AdminPasswordResetRequestIn | None = None,
    db: Any = Depends(get_db),
) -> AdminSessionOut:
    from tigrbl_identity_admin.bootstrap import issue_password_reset_token, user_is_admin
    from tigrbl_identity_runtime.settings import settings

    if payload is None:
        payload = AdminPasswordResetRequestIn.model_validate(await request.json() or {})
    row = await _find_user_by_identifier(db, payload.identifier)
    debug_token = None
    if row is not None and user_is_admin(row):
        debug_token = await issue_password_reset_token(user=row, db=db)
        if not settings.admin_password_reset_debug_disclosure:
            debug_token = None
    return _admin_session_payload(None, debug_reset_token=debug_token)


@admin_api.route("/admin/auth/reset-password", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_reset_password(
    request: Request,
    payload: AdminPasswordResetCompleteIn | None = None,
    db: Any = Depends(get_db),
) -> Response:
    from tigrbl_identity_admin.bootstrap import consume_password_reset_token
    from tigrbl_identity_runtime.http_standards.cookies import clear_session_cookie

    if payload is None:
        payload = AdminPasswordResetCompleteIn.model_validate(await request.json() or {})
    user = await consume_password_reset_token(token=payload.token, new_password=payload.password, db=db)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid or expired reset token")
    response = JSONResponse(_admin_session_payload(None).model_dump())
    clear_session_cookie(response)
    return response


@admin_api.route("/admin/auth/change-password", methods=["POST"], response_model=AdminSessionOut, tags=ADMIN_AUTH_TAGS)
async def admin_change_password(
    request: Request,
    payload: AdminPasswordChangeIn | None = None,
    db: Any = Depends(get_db),
) -> AdminSessionOut:
    if payload is None:
        payload = AdminPasswordChangeIn.model_validate(await request.json() or {})
    session_row, user = await _resolve_admin_session_and_user(request, db)
    if not user.verify_password(payload.current_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid current password")
    row = await read_record(User, db, user.id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    row = await update_record(
        User,
        db,
        row.id,
        {
            "password_hash": hash_pw(payload.new_password),
            "must_change_password": False,
            "password_reset_token_hash": None,
            "password_reset_expires_at": None,
        },
    )
    return _admin_session_payload(row, session_id=str(session_row.id))


__all__ = [
    "admin_change_password",
    "admin_forgot_password",
    "admin_login",
    "admin_login_browser_redirect",
    "admin_logout",
    "admin_reset_password",
    "admin_session",
]
