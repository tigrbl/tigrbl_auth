"""Authorization code model with browser-session linkage."""

from __future__ import annotations

import datetime as dt
from typing import Any
from typing import Optional

from tigrbl.security import Depends as TigrblDepends
from tigrbl_identity_storage.framework import (
    AsyncSession,
    Base,
    Request,
    TenantColumn,
    Timestamped,
    TigrblRouter,
    UserColumn,
    S,
    acol,
    ForeignKeySpec,
    JSON,
    PgUUID,
    String,
    TZDateTime,
    Mapped,
    UUID,
    GUIDPk,
)
from .._ops import create_record, read_record, record_id, update_record, utc_now
from ..engine import get_db


class AuthCode(Base, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "auth_codes"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False)
    )
    session_id: Mapped[UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.sessions.id"), nullable=True, index=True)
    )
    redirect_uri: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    code_challenge: Mapped[str | None] = acol(storage=S(String, nullable=True))
    nonce: Mapped[str | None] = acol(storage=S(String, nullable=True))
    scope: Mapped[str | None] = acol(storage=S(String, nullable=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def create_for_authorization(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID,
        client_id: UUID,
        redirect_uri: str,
        expires_at: dt.datetime,
        session_id: UUID | None = None,
        code_challenge: str | None = None,
        nonce: str | None = None,
        scope: str | None = None,
        claims: dict | None = None,
    ) -> "AuthCode":
        return await create_record(
            cls,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "session_id": session_id,
                "redirect_uri": redirect_uri,
                "code_challenge": code_challenge,
                "nonce": nonce,
                "scope": scope,
                "expires_at": expires_at,
                "claims": claims,
            },
        )

    @classmethod
    async def consume(cls, db: Any, *, code_id: UUID) -> "AuthCode | None":
        row = await read_record(cls, db, code_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row) or code_id, {"expires_at": utc_now()})

    @classmethod
    async def expire(cls, db: Any, *, code_id: UUID) -> "AuthCode | None":
        row = await read_record(cls, db, code_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row) or code_id, {"expires_at": utc_now()})


api = router = TigrblRouter()


@api.route("/authorize", methods=["GET"])
async def authorize(
    request: Request,
    response_type: str | None = None,
    client_id: str | None = None,
    redirect_uri: str | None = None,
    scope: str | None = None,
    response_mode: Optional[str] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
    prompt: Optional[str] = None,
    max_age: Optional[int] = None,
    login_hint: Optional[str] = None,
    claims: Optional[str] = None,
    request_uri: Optional[str] = None,
    request_object: Optional[str] = None,
    authorization_details: Optional[str] = None,
    db: AsyncSession = TigrblDepends(get_db),
) -> Any:
    from ._op import authorize_request

    params = {
        "response_type": response_type or request.query_params.get("response_type"),
        "client_id": client_id or request.query_params.get("client_id"),
        "redirect_uri": redirect_uri or request.query_params.get("redirect_uri"),
        "scope": scope or request.query_params.get("scope"),
        "response_mode": response_mode or request.query_params.get("response_mode"),
        "state": state or request.query_params.get("state"),
        "nonce": nonce or request.query_params.get("nonce"),
        "code_challenge": code_challenge or request.query_params.get("code_challenge"),
        "code_challenge_method": code_challenge_method or request.query_params.get("code_challenge_method"),
        "prompt": prompt or request.query_params.get("prompt"),
        "max_age": max_age if max_age is not None else request.query_params.get("max_age"),
        "login_hint": login_hint or request.query_params.get("login_hint"),
        "claims": claims or request.query_params.get("claims"),
        "request_uri": request_uri or request.query_params.get("request_uri"),
        "request": request_object or request.query_params.get("request"),
        "authorization_details": authorization_details or request.query_params.get("authorization_details"),
        "resource": list(request.query_params.getlist("resource"))
        if hasattr(request.query_params, "getlist")
        else None,
    }
    return await authorize_request(request=request, db=db, params=params)


AuthCode.authorize = staticmethod(authorize)  # type: ignore[attr-defined]


__all__ = ["AuthCode", "api", "router", "authorize"]
