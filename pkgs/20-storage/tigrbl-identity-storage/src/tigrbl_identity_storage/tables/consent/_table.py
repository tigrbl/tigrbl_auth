"""Durable consent records for scopes and claims grants."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_server.framework import (
    Base,
    BaseModel,
    Depends,
    HTTPException,
    Request,
    TenantColumn,
    Timestamped,
    TigrblRouter,
    UserColumn,
    S,
    acol,
    JSON,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
    status,
)
from ..user import MyAccountMutationOut, User, _current_principal_dependency, _iso, _not_found_uuid
from .._ops import create_record, field, list_records, read_record, record_id, update_record, utc_now
from ..engine import get_db


class MyAccountConsentOut(BaseModel):
    id: str
    tenant_id: str
    user_id: str
    client_id: str
    scope: str
    claims: dict[str, Any] | None = None
    state: str = "active"
    granted_at: str | None = None
    expires_at: str | None = None
    revoked_at: str | None = None


class MyAccountAuthorizedAppOut(BaseModel):
    client_id: str
    tenant_id: str
    scope: str
    consent_state: str = "active"
    granted_at: str | None = None
    revoked_at: str | None = None


class Consent(Base, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "consents"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False, index=True)
    )
    scope: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    state: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active"))
    granted_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

    @classmethod
    async def grant(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID,
        client_id: UUID,
        scope: str,
        claims: dict | None = None,
        expires_at: dt.datetime | None = None,
    ) -> "Consent":
        return await create_record(
            cls,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "scope": scope,
                "claims": claims,
                "state": "active",
                "granted_at": utc_now(),
                "expires_at": expires_at,
            },
        )

    @classmethod
    async def list_for_user(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID | None = None,
        active_only: bool = True,
    ) -> list["Consent"]:
        filters: dict[str, Any] = {"user_id": user_id}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        rows = await list_records(cls, db, filters)
        if not active_only:
            return rows
        now = utc_now()
        return [
            row
            for row in rows
            if field(row, "state", "active") == "active"
            and field(row, "revoked_at") is None
            and (field(row, "expires_at") is None or field(row, "expires_at") > now)
        ]

    @classmethod
    async def revoke_for_user(
        cls,
        db: Any,
        *,
        consent_id: UUID,
        user_id: UUID | None = None,
    ) -> "Consent | None":
        row = await read_record(cls, db, consent_id)
        if row is None or (user_id is not None and str(field(row, "user_id")) != str(user_id)):
            return None
        return await update_record(cls, db, record_id(row) or consent_id, {"state": "revoked", "revoked_at": utc_now()})

    @classmethod
    async def revoke_for_client(
        cls,
        db: Any,
        *,
        client_id: UUID,
        user_id: UUID | None = None,
        tenant_id: UUID | None = None,
    ) -> list["Consent"]:
        filters: dict[str, Any] = {"client_id": client_id}
        if user_id is not None:
            filters["user_id"] = user_id
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        revoked = []
        for row in await list_records(cls, db, filters):
            updated = await update_record(cls, db, record_id(row), {"state": "revoked", "revoked_at": utc_now()})
            revoked.append(updated)
        return revoked


account_api = account_router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


def _consent_payload(consent: Consent) -> MyAccountConsentOut:
    return MyAccountConsentOut(
        id=str(consent.id),
        tenant_id=str(consent.tenant_id),
        user_id=str(consent.user_id),
        client_id=str(consent.client_id),
        scope=str(consent.scope),
        claims=consent.claims,
        state=str(consent.state or "active"),
        granted_at=_iso(getattr(consent, "granted_at", None)),
        expires_at=_iso(getattr(consent, "expires_at", None)),
        revoked_at=_iso(getattr(consent, "revoked_at", None)),
    )


@account_api.route(
    "/account/consents",
    methods=["GET"],
    response_model=list[MyAccountConsentOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_consents(
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountConsentOut]:
    rows = await list_records(
        Consent,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [_consent_payload(row) for row in rows]


@account_api.route(
    "/account/consents/{consent_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_consent(
    consent_id: str,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    consent_uuid = _not_found_uuid(consent_id, field="consent")
    row = await read_record(Consent, db, consent_uuid)
    if row is not None and (
        str(getattr(row, "user_id", "")) != str(current_user.id)
        or str(getattr(row, "tenant_id", "")) != str(current_user.tenant_id)
    ):
        row = None
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "consent not found")
    updated = await update_record(
        Consent,
        db,
        row.id,
        {"state": "revoked", "revoked_at": row.revoked_at or utc_now()},
    )
    return MyAccountMutationOut(status="revoked", id=str(updated.id))


@account_api.route(
    "/account/authorized-apps",
    methods=["GET"],
    response_model=list[MyAccountAuthorizedAppOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_authorized_apps(
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountAuthorizedAppOut]:
    rows = await list_records(
        Consent,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [
        MyAccountAuthorizedAppOut(
            client_id=str(row.client_id),
            tenant_id=str(row.tenant_id),
            scope=str(row.scope),
            consent_state=str(row.state or "active"),
            granted_at=_iso(getattr(row, "granted_at", None)),
            revoked_at=_iso(getattr(row, "revoked_at", None)),
        )
        for row in rows
    ]


@account_api.route(
    "/account/authorized-apps/{client_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_authorized_app(
    client_id: str,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    client_uuid = _not_found_uuid(client_id, field="client")
    rows = await list_records(
        Consent,
        db,
        {
            "client_id": client_uuid,
            "user_id": current_user.id,
            "tenant_id": current_user.tenant_id,
        },
    )
    if not rows:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "authorized app not found")
    now = utc_now()
    for row in rows:
        await update_record(
            Consent,
            db,
            row.id,
            {"state": "revoked", "revoked_at": row.revoked_at or now},
        )
    return MyAccountMutationOut(status="revoked", id=str(client_uuid))


Consent.list_account_consents = staticmethod(list_account_consents)  # type: ignore[attr-defined]
Consent.revoke_account_consent = staticmethod(revoke_account_consent)  # type: ignore[attr-defined]
Consent.list_account_authorized_apps = staticmethod(list_account_authorized_apps)  # type: ignore[attr-defined]
Consent.revoke_account_authorized_app = staticmethod(revoke_account_authorized_app)  # type: ignore[attr-defined]


__all__ = [
    "Consent",
    "MyAccountAuthorizedAppOut",
    "MyAccountConsentOut",
    "account_api",
    "account_router",
    "list_account_authorized_apps",
    "list_account_consents",
    "revoke_account_authorized_app",
    "revoke_account_consent",
]
