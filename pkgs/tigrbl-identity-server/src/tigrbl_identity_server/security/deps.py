"""
tigrbl_identity_server.security.deps
========================

Tigrbl dependency helpers used by the AuthN service itself
and by *any* downstream service that wishes to rely on AuthN’s
JWT / API-key semantics.

Exports
-------
get_current_principal   → dependency that returns an authenticated **User**
require_scope           → decorator enforcing coarse scopes

Both helpers are **framework-thin**: they translate `AuthError` raised by
`backends.py` into `tigrbl.types.HTTPException` and nothing more.
"""

from __future__ import annotations

from tigrbl_identity_server.framework import (
    Depends,
    Header,
    HTTPException,
    Request,
    status,
    AsyncSession,
    select,
)
from tigrbl_identity_runtime.deployment import deployment_from_request

from tigrbl_authn_credentials.backends import (
    ApiKeyBackend,
    AuthError,
    PasswordBackend,
)  # PasswordBackend not used here, but re-exported for completeness

from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_authn_credentials.token_service import JWTCoder, InvalidTokenError
from tigrbl_identity_storage.tables import User
from tigrbl_identity_server.security.context import principal_var
from tigrbl_auth_protocol_oidc.standards.session_mgmt import resolve_browser_session
from tigrbl_auth_protocol_oauth.standards.rfc6750 import extract_bearer_token
from tigrbl_auth_protocol_oauth.standards.rfc9700 import runtime_security_profile, verify_access_token_sender_constraint
from tigrbl_auth_protocol_oauth.standards.mtls import presented_certificate_thumbprint
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_core.typing import Principal


# ---------------------------------------------------------------------
# Backends + Coder
# ---------------------------------------------------------------------
_api_key_backend = ApiKeyBackend()
_jwt_coder = JWTCoder.default()


# ---------------------------------------------------------------------
# Tigrbl dependencies
# ---------------------------------------------------------------------
async def _user_from_jwt(token: str, db: AsyncSession, *, cert_thumbprint: str | None = None) -> User | None:
    try:
        payload = await _jwt_coder.async_decode(token, cert_thumbprint=cert_thumbprint)
    except InvalidTokenError:
        return None

    users = await User.handlers.list.core(
        {
            "payload": {
                "filters": {
                    "id": payload["sub"],
                    "is_active": True,
                }
            },
            "db": db,
        }
    )
    if hasattr(users, "items"):
        users = users.items
    if isinstance(users, (list, tuple)):
        return users[0] if users else None

    # Fallback for dependency-light runtimes that expose scalar() only.
    return await db.scalar(select(User).where(User.id == payload["sub"], User.is_active.is_(True)))


async def _user_from_api_key(raw_key: str, db: AsyncSession) -> Principal | None:
    try:
        principal, _ = await _api_key_backend.authenticate(db, raw_key)
        return principal
    except AuthError:
        return None


async def _user_from_browser_session(request: Request, db: AsyncSession) -> User | None:
    session = await resolve_browser_session(request)
    if session is None:
        return None
    return await db.scalar(select(User).where(User.id == session.user_id, User.is_active.is_(True)))


# ---------------------------------------------------------------------
# NEW — AuthNProvider‑compatible helper
# ---------------------------------------------------------------------
async def get_principal(  # <-- Tigrbl calls this
    request: Request,
    authorization: str = Header("", alias="Authorization"),
    api_key: str | None = Header(None, alias="x-api-key"),
    dpop: str | None = Header(None, alias="DPoP"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Return a lightweight principal dict that Tigrbl understands:
        { "sub": "<user_id>", "tid": "<tenant_id>" }
    Raises HTTP 401 on failure.
    """
    user = await get_current_principal(  # reuse the existing logic
        request,
        authorization=authorization,
        api_key=api_key,
        dpop=dpop,
        db=db,
    )
    principal = {"sub": str(user.id), "tid": str(user.tenant_id)}

    # cache in both request.state and ContextVar
    request.state.principal = principal
    principal_var.set(principal)
    return principal


async def get_current_principal(  # type: ignore[override]
    request: Request,
    authorization: str = Header("", alias="Authorization"),
    api_key: str | None = Header(None, alias="x-api-key"),
    dpop: str | None = Header(None, alias="DPoP"),
    db: AsyncSession = Depends(get_db),
) -> Principal:
    """
    Resolve the request principal via **exactly one** of:

    1. `x-api-key:`  → ApiKeyBackend
    2. `Authorization: Bearer <jwt>`  → verified JWT

    On success
    ----------
    Returns the principal ORM instance (which satisfies ``Principal`` Protocol).

    On failure
    ----------
    Raises HTTP 401 (unauthenticated).
    """
    if api_key:
        if user := await _user_from_api_key(api_key, db):
            return user
    if user := await _user_from_browser_session(request, db):
        return user

    token = await extract_bearer_token(request, authorization)
    if token:
        cert_thumbprint = presented_certificate_thumbprint(request)
        user = await _user_from_jwt(token, db, cert_thumbprint=cert_thumbprint)
        if user:
            proof = dpop if isinstance(dpop, str) and dpop.strip() else None
            deployment = deployment_from_request(request, settings)
            policy = runtime_security_profile(deployment)
            if not (policy.sender_constraint_required or proof or cert_thumbprint):
                return user
            try:
                payload = await _jwt_coder.async_decode(token, cert_thumbprint=cert_thumbprint)
                verify_access_token_sender_constraint(
                    request,
                    payload,
                    deployment,
                    access_token=token,
                    dpop_proof=proof,
                )
            except InvalidTokenError:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")
            except Exception as exc:
                detail = getattr(exc, 'description', 'invalid token')
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail) from exc
            return user


    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "invalid or missing credentials",
        headers={"WWW-Authenticate": 'Bearer realm="authn"'},
    )


# Public re-exports
__all__ = [
    "get_current_principal",
    "get_principal",  # <- NEW
    "principal_var",  # <- used by row_filters
    "PasswordBackend",
    "ApiKeyBackend",
]
