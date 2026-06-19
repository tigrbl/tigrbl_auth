"""Device code model with durable authorization lifecycle fields."""

from __future__ import annotations

import datetime as dt
import uuid
from pathlib import Path
from typing import Any

from tigrbl_identity_server.framework import (
    Base,
    Depends,
    Timestamped,
    TigrblRouter,
    S,
    acol,
    ForeignKeySpec,
    Boolean,
    Integer,
    Mapped,
    PgUUID,
    String,
    TZDateTime,
    GUIDPk,
)
from tigrbl_identity_contracts.rest import DeviceAuthorizationOut
from ._ops import create_record, field, first_record, read_record, record_id, update_record, utc_now
from .engine import get_db


class DeviceCode(Base, GUIDPk, Timestamped):
    __tablename__ = "device_codes"
    __table_args__ = ({"schema": "authn"},)

    device_code: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True))
    user_code: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    client_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False)
    )
    scope: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    audience: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    resource: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False))
    interval: Mapped[int] = acol(storage=S(Integer, nullable=False))
    poll_count: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0))
    slow_down_count: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0))
    last_polled_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    authorized: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    authorized_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    denied_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    denial_reason: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    user_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.users.id"), nullable=True, index=True)
    )
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )

    @classmethod
    async def create_device_authorization(
        cls,
        db: Any,
        *,
        device_code: str,
        user_code: str,
        client_id: uuid.UUID,
        expires_at: dt.datetime,
        interval: int = 5,
        scope: str | None = None,
        audience: str | None = None,
        resource: str | None = None,
        tenant_id: uuid.UUID | None = None,
    ) -> "DeviceCode":
        return await create_record(
            cls,
            db,
            {
                "device_code": device_code,
                "user_code": user_code,
                "client_id": client_id,
                "scope": scope,
                "audience": audience,
                "resource": resource,
                "expires_at": expires_at,
                "interval": interval,
                "tenant_id": tenant_id,
            },
        )

    @classmethod
    async def approve(
        cls,
        db: Any,
        *,
        user_id: uuid.UUID,
        user_code: str | None = None,
        device_code: str | None = None,
        id: Any | None = None,
        tenant_id: uuid.UUID | None = None,
    ) -> "DeviceCode | None":
        row = await read_record(cls, db, id) if id is not None else None
        if row is None:
            lookup_code = device_code or (str(id) if id is not None else None)
            row = await first_record(cls, db, {"device_code": lookup_code} if lookup_code else {"user_code": user_code})
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {
                "authorized": True,
                "authorized_at": utc_now(),
                "user_id": user_id,
                "tenant_id": tenant_id or field(row, "tenant_id"),
                "last_polled_at": None,
            },
        )

    @classmethod
    async def deny(
        cls,
        db: Any,
        *,
        user_code: str | None = None,
        device_code: str | None = None,
        id: Any | None = None,
        reason: str | None = None,
    ) -> "DeviceCode | None":
        row = await read_record(cls, db, id) if id is not None else None
        if row is None:
            lookup_code = device_code or (str(id) if id is not None else None)
            row = await first_record(cls, db, {"device_code": lookup_code} if lookup_code else {"user_code": user_code})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"denied_at": utc_now(), "denial_reason": reason})

    @classmethod
    async def poll(cls, db: Any, *, device_code: str) -> "DeviceCode | None":
        row = await first_record(cls, db, {"device_code": device_code})
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {"poll_count": int(field(row, "poll_count", 0) or 0) + 1, "last_polled_at": utc_now()},
        )

    @classmethod
    async def consume(cls, db: Any, *, device_code: str) -> "DeviceCode | None":
        row = await first_record(cls, db, {"device_code": device_code})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"consumed_at": utc_now()})


api = router = TigrblRouter()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


@api.route("/device_authorization", methods=["POST"], response_model=DeviceAuthorizationOut)
async def device_authorization(request: Any, db: Any = Depends(get_db)) -> Any:
    from ._oauth_device_authorization import device_authorization_request

    result = await device_authorization_request(request=request, db=db)
    from tigrbl_authn_credentials.session_service import observe_device_authorization_response

    payload = result if isinstance(result, dict) else getattr(result, "model_dump", lambda **_: {})(mode="json")
    observe_device_authorization_response(_repo_root(), device_code=payload.get("device_code"), details=payload)
    return result


DeviceCode.device_authorization = staticmethod(device_authorization)  # type: ignore[attr-defined]

from ._device_code_hooks import approve_device_code, deny_device_code


__all__ = ["DeviceCode", "api", "router", "device_authorization", "approve_device_code", "deny_device_code"]
