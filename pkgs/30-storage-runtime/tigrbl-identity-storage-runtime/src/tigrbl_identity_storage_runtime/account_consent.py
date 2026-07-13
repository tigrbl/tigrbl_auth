"""Runtime-owned my-account consent routes."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Depends, HTTPException, TigrblRouter, status
from tigrbl_identity_storage.tables.consent import Consent
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage.tables.user import User, _current_principal_dependency, _not_found_uuid

from .ops.consents import (
    list_consents_for_user,
    revoke_consent_for_user,
    revoke_consents_for_client,
)

api = router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


@api.route(
    "/account/consents",
    methods=["GET"],
    response_model=list[Consent.schemas.list.out],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_consents(
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[Consent]:
    return await list_consents_for_user(
        {
            "payload": {
                "user_id": current_user.id,
                "tenant_id": current_user.tenant_id,
            },
            "db": db,
        }
    )


@api.route(
    "/account/consents/{consent_id}",
    methods=["DELETE"],
    response_model=Consent.schemas.update.out,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_consent(
    consent_id: str,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> Consent:
    row = await revoke_consent_for_user(
        {
            "path_params": {
                "id": _not_found_uuid(consent_id, field="consent"),
            },
            "payload": {
                "user_id": current_user.id,
                "tenant_id": current_user.tenant_id,
            },
            "db": db,
        }
    )
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "consent not found")
    return row


@api.route(
    "/account/authorized-apps",
    methods=["GET"],
    response_model=list[Consent.schemas.list.out],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_authorized_apps(
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[Consent]:
    return await list_consents_for_user(
        {
            "payload": {
                "user_id": current_user.id,
                "tenant_id": current_user.tenant_id,
            },
            "db": db,
        }
    )


@api.route(
    "/account/authorized-apps/{client_id}",
    methods=["DELETE"],
    response_model=list[Consent.schemas.update.out],
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_authorized_app(
    client_id: str,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[Consent]:
    rows = await revoke_consents_for_client(
        {
            "path_params": {
                "client_id": _not_found_uuid(client_id, field="client"),
            },
            "payload": {
                "user_id": current_user.id,
                "tenant_id": current_user.tenant_id,
            },
            "db": db,
        }
    )
    if not rows:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "authorized app not found")
    return rows


__all__ = [
    "api",
    "list_account_authorized_apps",
    "list_account_consents",
    "revoke_account_authorized_app",
    "revoke_account_consent",
    "router",
]
