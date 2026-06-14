"""Pushed authorization request model with durable lifecycle fields."""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import datetime, timedelta, timezone

from tigrbl_identity_server.framework import (
    Base,
    Timestamped,
    S,
    acol,
    JSON,
    Mapped,
    String,
    Integer,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_server.framework import HTTPException
from http import HTTPStatus as status

DEFAULT_PAR_EXPIRY = 90


def _utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def _default_request_uri() -> str:
    return f"urn:ietf:params:oauth:request_uri:{uuid.uuid4()}"


def _default_expires_in() -> int:
    return DEFAULT_PAR_EXPIRY


def _default_expires_at() -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=_default_expires_in())


class PushedAuthorizationRequest(Base, GUIDPk, Timestamped):
    __tablename__ = "par_requests"
    __table_args__ = ({"schema": "authn"},)

    request_uri: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, default=_default_request_uri))
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    params: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    expires_in: Mapped[int] = acol(storage=S(Integer, nullable=False, default=_default_expires_in))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, default=_default_expires_at))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


    @property
    def one_time_use(self) -> bool:
        return True

    def is_expired(self, *, now: datetime | None = None) -> bool:
        current = _utc(now) or datetime.now(tz=timezone.utc)
        expires_at = _utc(self.expires_at)
        return expires_at is not None and expires_at <= current

    def is_consumed(self) -> bool:
        return _utc(self.consumed_at) is not None

    def client_bound(self, client_id: uuid.UUID | str | None) -> bool:
        if self.client_id is None or client_id in {None, ''}:
            return True
        return str(self.client_id) == str(client_id)

    def consume(self, *, now: datetime | None = None) -> datetime:
        consumed_at = _utc(now) or datetime.now(tz=timezone.utc)
        self.consumed_at = consumed_at
        return consumed_at

    @staticmethod
    async def _extract_form_params(context: dict) -> dict:
        if not settings.enable_rfc9126:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PAR disabled")
        request = context.get("request")
        if request is None:
            return {}
        form = await request.form()
        return dict(form or {})


__all__ = ["PushedAuthorizationRequest", "DEFAULT_PAR_EXPIRY"]
