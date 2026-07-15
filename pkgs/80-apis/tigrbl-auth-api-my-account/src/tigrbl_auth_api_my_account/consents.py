"""Current-subject consent and authorized-application routes."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from tigrbl import TigrblRouter
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_storage.tables import User
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.consents import (
    list_consents_for_user,
    revoke_consent_for_user,
    revoke_consents_for_client,
)
from tigrbl_identity_storage_runtime.ops.common import field_value

from .common import current_principal_dependency, not_found_uuid


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


def _consent_payload(row: Any) -> MyAccountConsentOut:
    return MyAccountConsentOut(
        id=field_value(row, "id"),
        tenant_id=field_value(row, "tenant_id"),
        user_id=field_value(row, "user_id"),
        client_id=field_value(row, "client_id"),
        scope=str(field_value(row, "scope", "")),
        claims=field_value(row, "claims"),
        state=str(field_value(row, "state", "active")),
        granted_at=field_value(row, "granted_at"),
        expires_at=field_value(row, "expires_at"),
        revoked_at=field_value(row, "revoked_at"),
    )


def _authorized_app_payload(row: Any) -> MyAccountAuthorizedAppOut:
    return MyAccountAuthorizedAppOut(
        client_id=field_value(row, "client_id"),
        tenant_id=field_value(row, "tenant_id"),
        scope=str(field_value(row, "scope", "")),
        consent_state=str(field_value(row, "state", "active")),
        granted_at=field_value(row, "granted_at"),
        revoked_at=field_value(row, "revoked_at"),
    )


@api.route(
    "/account/consents",
    methods=["GET"],
    response_model=list[MyAccountConsentOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_consents(
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountConsentOut]:
    rows = await list_consents_for_user(
        {"payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id}, "db": db}
    )
    return [_consent_payload(row) for row in rows]


@api.route(
    "/account/consents/{consent_id}",
    methods=["DELETE"],
    response_model=MyAccountConsentOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_consent(
    consent_id: str,
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountConsentOut:
    row = await revoke_consent_for_user(
        {
            "path_params": {"id": not_found_uuid(consent_id, field="consent")},
            "payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
            "db": db,
        }
    )
    if row is None:
        raise HTTPException(404, "consent not found")
    return _consent_payload(row)


@api.route(
    "/account/authorized-apps",
    methods=["GET"],
    response_model=list[MyAccountAuthorizedAppOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_authorized_apps(
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountAuthorizedAppOut]:
    rows = await list_consents_for_user(
        {"payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id}, "db": db}
    )
    return [_authorized_app_payload(row) for row in rows]


@api.route(
    "/account/authorized-apps/{client_id}",
    methods=["DELETE"],
    response_model=list[MyAccountConsentOut],
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_authorized_app(
    client_id: str,
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountConsentOut]:
    rows = await revoke_consents_for_client(
        {
            "path_params": {"client_id": not_found_uuid(client_id, field="client")},
            "payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
            "db": db,
        }
    )
    if not rows:
        raise HTTPException(404, "authorized app not found")
    return [_consent_payload(row) for row in rows]


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
