"""Certified-core auth dependency helpers."""

from __future__ import annotations

from http import HTTPStatus as status
from tigrbl.core.crud.params import Header
from tigrbl.engine import HybridSession as AsyncSession
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_server.security.context import principal_var
from tigrbl_identity_server.security.user_lookup import first_user_by_filters
from tigrbl_auth_protocol_oidc.standards.session_mgmt import resolve_browser_session
from tigrbl_authn_credentials.backends import ApiKeyBackend, AuthError, PasswordBackend
from tigrbl_authn_credentials.token_service import JWTCoder, InvalidTokenError
from tigrbl_auth_protocol_oauth.standards.mtls import presented_certificate_thumbprint
from tigrbl_auth_protocol_oauth.standards.bearer_token_usage import extract_bearer_token
from tigrbl_auth_protocol_oauth.standards.rfc9700 import verify_access_token_sender_constraint
from tigrbl_identity_storage.tables import User
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_core.typing import Principal

_api_key_backend = ApiKeyBackend()
_jwt_coder: JWTCoder | None = None


async def _get_jwt_coder() -> JWTCoder:
    global _jwt_coder
    if _jwt_coder is None:
        _jwt_coder = await JWTCoder.async_default()
    return _jwt_coder


async def _user_from_jwt(token: str, db: AsyncSession, *, cert_thumbprint: str | None = None) -> User | None:
    try:
        payload = await (await _get_jwt_coder()).async_decode(token, cert_thumbprint=cert_thumbprint)
    except InvalidTokenError:
        return None
    return await first_user_by_filters(db, {"id": payload["sub"], "is_active": True})


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
    return await first_user_by_filters(db, {"id": session.user_id, "is_active": True})


async def get_principal(
    request: Request,
    authorization: str = Header("", alias="Authorization"),
    api_key: str | None = Header(None, alias="x-api-key"),
    dpop: str | None = Header(None, alias="DPoP"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await get_current_principal(
        request,
        authorization=authorization,
        api_key=api_key,
        dpop=dpop,
        db=db,
    )
    principal = {"sub": str(user.id), "tid": str(user.tenant_id)}
    request.state.principal = principal
    principal_var.set(principal)
    return principal


async def get_current_principal(
    request: Request,
    authorization: str = Header("", alias="Authorization"),
    api_key: str | None = Header(None, alias="x-api-key"),
    dpop: str | None = Header(None, alias="DPoP"),
    db: AsyncSession = Depends(get_db),
) -> Principal:
    if api_key:
        if user := await _user_from_api_key(api_key, db):
            return user
    if user := await _user_from_browser_session(request, db):
        return user
    token = await extract_bearer_token(request, authorization)
    if token:
        cert_thumbprint = presented_certificate_thumbprint(request)
        try:
            payload = await (await _get_jwt_coder()).async_decode(token, cert_thumbprint=cert_thumbprint)
        except InvalidTokenError as exc:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token") from exc

        try:
            verify_access_token_sender_constraint(
                request,
                payload,
                deployment_from_request(request, settings),
                access_token=token,
                dpop_proof=dpop,
            )
        except Exception as exc:
            detail = getattr(exc, 'description', 'invalid token')
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail) from exc

        if user := await _user_from_jwt(token, db, cert_thumbprint=cert_thumbprint):
            return user
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "invalid or missing credentials",
        headers={"WWW-Authenticate": 'Bearer realm="authn"'},
    )


__all__ = [
    "get_current_principal",
    "get_principal",
    "principal_var",
    "PasswordBackend",
    "ApiKeyBackend",
]
