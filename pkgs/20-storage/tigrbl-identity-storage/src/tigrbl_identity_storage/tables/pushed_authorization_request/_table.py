"""Pushed authorization request model with durable lifecycle fields."""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    Depends,
    Timestamped,
    TigrblRouter,
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
from tigrbl_identity_storage.framework import HTTPException
from http import HTTPStatus as status
from .._ops import create_record, first_record, record_id, update_record
from ..engine import get_db

DEFAULT_PAR_EXPIRY = 90


class PushedAuthorizationRequestIn(BaseModel):
    client_id: str
    request: str | None = None
    response_type: str | None = None
    redirect_uri: str | None = None
    scope: str | None = None
    state: str | None = None
    nonce: str | None = None
    code_challenge: str | None = None
    code_challenge_method: str | None = None
    resource: list[str] | None = None
    authorization_details: list[dict[str, Any]] | None = None


class PushedAuthorizationResponse(BaseModel):
    request_uri: str
    expires_in: int


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


class PushedAuthorizationRequest(RestOltpTable, GUIDPk, Timestamped):
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

    @classmethod
    async def create_request(
        cls,
        db: Any,
        *,
        params: dict,
        client_id: uuid.UUID | None = None,
        tenant_id: uuid.UUID | None = None,
        request_uri: str | None = None,
        expires_in: int | None = None,
        expires_at: datetime | None = None,
    ) -> "PushedAuthorizationRequest":
        ttl = expires_in or _default_expires_in()
        return await create_record(
            cls,
            db,
            {
                "request_uri": request_uri or _default_request_uri(),
                "client_id": client_id,
                "tenant_id": tenant_id,
                "params": dict(params),
                "expires_in": ttl,
                "expires_at": expires_at or datetime.now(tz=timezone.utc) + timedelta(seconds=ttl),
            },
        )

    @classmethod
    async def resolve_request_uri(
        cls,
        db: Any,
        *,
        request_uri: str,
        client_id: uuid.UUID | str | None = None,
    ) -> "PushedAuthorizationRequest | None":
        row = await first_record(cls, db, {"request_uri": request_uri})
        if row is None or row.is_expired() or row.is_consumed() or not row.client_bound(client_id):
            return None
        return row

    @classmethod
    async def consume_request(cls, db: Any, *, request_uri: str) -> "PushedAuthorizationRequest | None":
        row = await first_record(cls, db, {"request_uri": request_uri})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"consumed_at": datetime.now(tz=timezone.utc)})


api = router = TigrblRouter()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


@api.route("/par", methods=["POST"], response_model=PushedAuthorizationResponse)
async def par(request: Any, db: Any = Depends(get_db)) -> Any:
    from ._op import pushed_authorization_request

    result = await pushed_authorization_request(request=request, db=db)
    from tigrbl_identity_storage.session_service import observe_par_response

    payload = result if isinstance(result, dict) else getattr(result, "model_dump", lambda **_: {})(mode="json")
    observe_par_response(_repo_root(), request_uri=payload.get("request_uri"), details=payload)
    return result


PushedAuthorizationRequest.par = staticmethod(par)  # type: ignore[attr-defined]


__all__ = [
    "DEFAULT_PAR_EXPIRY",
    "PushedAuthorizationRequest",
    "PushedAuthorizationRequestIn",
    "PushedAuthorizationResponse",
    "api",
    "router",
    "par",
]
