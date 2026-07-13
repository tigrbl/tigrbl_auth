"""Current-subject consent and authorized-application routes."""

from __future__ import annotations

from typing import Any

from tigrbl import TigrblRouter
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_storage.tables import Consent, User
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage_runtime.ops.consents import (
    list_consents_for_user,
    revoke_consent_for_user,
    revoke_consents_for_client,
)

from .common import current_principal_dependency, not_found_uuid


api = router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


@api.route(
    "/account/consents",
    methods=["GET"],
    response_model=list[Consent.schemas.list.out],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_consents(
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[Consent]:
    return await list_consents_for_user(
        {"payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id}, "db": db}
    )


@api.route(
    "/account/consents/{consent_id}",
    methods=["DELETE"],
    response_model=Consent.schemas.update.out,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_consent(
    consent_id: str,
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> Consent:
    row = await revoke_consent_for_user(
        {
            "path_params": {"id": not_found_uuid(consent_id, field="consent")},
            "payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
            "db": db,
        }
    )
    if row is None:
        raise HTTPException(404, "consent not found")
    return row


@api.route(
    "/account/authorized-apps",
    methods=["GET"],
    response_model=list[Consent.schemas.list.out],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_authorized_apps(
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[Consent]:
    return await list_account_consents(current_user=current_user, db=db)


@api.route(
    "/account/authorized-apps/{client_id}",
    methods=["DELETE"],
    response_model=list[Consent.schemas.update.out],
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_authorized_app(
    client_id: str,
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[Consent]:
    rows = await revoke_consents_for_client(
        {
            "path_params": {"client_id": not_found_uuid(client_id, field="client")},
            "payload": {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
            "db": db,
        }
    )
    if not rows:
        raise HTTPException(404, "authorized app not found")
    return rows


__all__ = [
    "api",
    "list_account_authorized_apps",
    "list_account_consents",
    "revoke_account_authorized_app",
    "revoke_account_consent",
    "router",
]
