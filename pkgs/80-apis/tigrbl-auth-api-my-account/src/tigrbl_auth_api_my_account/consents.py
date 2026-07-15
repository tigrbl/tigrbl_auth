"""Current-subject consent and authorized-application HTTP routes."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_contracts.account_self_service import (
    AccountConsent,
    AccountNotFoundError,
    AccountPrincipal,
)
from tigrbl_identity_server.account_self_service import (
    account_principal,
    account_self_service_for_request,
    get_db,
)

from .common import current_principal_dependency


api = router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


class MyAccountConsentOut(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    client_id: UUID
    scope: str
    claims: dict[str, Any] | None = None
    state: str
    granted_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None


class MyAccountAuthorizedAppOut(BaseModel):
    client_id: UUID
    tenant_id: UUID
    scope: str
    consent_state: str
    granted_at: datetime | None = None
    revoked_at: datetime | None = None


def _consent_payload(record: AccountConsent) -> MyAccountConsentOut:
    return MyAccountConsentOut(
        id=record.consent_id,
        tenant_id=record.tenant_id,
        user_id=record.identity_id,
        client_id=record.client_id,
        scope=record.scope,
        claims=dict(record.claims) if record.claims is not None else None,
        state=record.state,
        granted_at=record.granted_at,
        expires_at=record.expires_at,
        revoked_at=record.revoked_at,
    )


def _authorized_app_payload(record: AccountConsent) -> MyAccountAuthorizedAppOut:
    return MyAccountAuthorizedAppOut(
        client_id=record.client_id,
        tenant_id=record.tenant_id,
        scope=record.scope,
        consent_state=record.state,
        granted_at=record.granted_at,
        revoked_at=record.revoked_at,
    )


@api.route(
    "/account/consents",
    methods=["GET"],
    response_model=list[MyAccountConsentOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_consents(
    request: Request | None = None,
    current_user: AccountPrincipal | object = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountConsentOut]:
    records = await account_self_service_for_request(
        request or object(), db
    ).list_consents(account_principal(current_user))
    return [_consent_payload(record) for record in records]


@api.route(
    "/account/consents/{consent_id}",
    methods=["DELETE"],
    response_model=MyAccountConsentOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_consent(
    consent_id: str,
    request: Request | None = None,
    current_user: AccountPrincipal | object = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountConsentOut:
    try:
        record = await account_self_service_for_request(
            request or object(), db
        ).revoke_consent(account_principal(current_user), consent_id)
    except AccountNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    return _consent_payload(record)


@api.route(
    "/account/authorized-apps",
    methods=["GET"],
    response_model=list[MyAccountAuthorizedAppOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_authorized_apps(
    request: Request | None = None,
    current_user: AccountPrincipal | object = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountAuthorizedAppOut]:
    records = await account_self_service_for_request(
        request or object(), db
    ).list_authorized_apps(account_principal(current_user))
    return [_authorized_app_payload(record) for record in records]


@api.route(
    "/account/authorized-apps/{client_id}",
    methods=["DELETE"],
    response_model=list[MyAccountConsentOut],
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_authorized_app(
    client_id: str,
    request: Request | None = None,
    current_user: AccountPrincipal | object = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountConsentOut]:
    try:
        records = await account_self_service_for_request(
            request or object(), db
        ).revoke_authorized_app(account_principal(current_user), client_id)
    except AccountNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    return [_consent_payload(record) for record in records]


__all__ = [
    "MyAccountAuthorizedAppOut",
    "MyAccountConsentOut",
    "api",
    "list_account_authorized_apps",
    "list_account_consents",
    "revoke_account_authorized_app",
    "revoke_account_consent",
    "router",
]
