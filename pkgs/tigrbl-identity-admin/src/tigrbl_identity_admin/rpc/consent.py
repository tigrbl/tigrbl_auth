"""Consent inspection and revocation RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from tigrbl_auth.api.rpc.schemas.consent import (
    ConsentListParams,
    ConsentListResult,
    ConsentRevokeParams,
    ConsentRevokeResult,
    ConsentShowParams,
    ConsentShowResult,
)
from tigrbl_auth.api.rpc.methods._shared import get_row, list_rows, row_to_dict


async def handle_consent_list(params: ConsentListParams, _context):
    from tigrbl_auth.tables import Consent

    rows = await list_rows(
        Consent,
        filters={"user_id": params.user_id, "client_id": params.client_id, "state": params.state},
        limit=params.limit,
        offset=params.offset,
        order_by="granted_at",
    )
    return ConsentListResult(count=len(rows), items=[row_to_dict(row) for row in rows])


async def handle_consent_show(params: ConsentShowParams, _context):
    from tigrbl_auth.tables import Consent

    row = await get_row(Consent, id_value=params.consent_id)
    return ConsentShowResult(consent=row_to_dict(row) if row else None)


async def handle_consent_revoke(params: ConsentRevokeParams, _context):
    from tigrbl_auth.services.persistence import revoke_consent_async

    row = await revoke_consent_async(params.consent_id)
    return ConsentRevokeResult(consent=row_to_dict(row) if row else None)


METHODS = (
    RpcMethodDefinition(
        name="consent.list",
        summary="List durable consent records.",
        description="Returns persisted consent grants for operator inspection.",
        params_model=ConsentListParams,
        result_model=ConsentListResult,
        handler=handle_consent_list,
        owner_module="tigrbl_auth/api/rpc/methods/consent.py",
        tags=("consent", "operator"),
    ),
    RpcMethodDefinition(
        name="consent.show",
        summary="Show a durable consent record.",
        description="Returns a single consent grant by identifier.",
        params_model=ConsentShowParams,
        result_model=ConsentShowResult,
        handler=handle_consent_show,
        owner_module="tigrbl_auth/api/rpc/methods/consent.py",
        tags=("consent", "operator"),
    ),
    RpcMethodDefinition(
        name="consent.revoke",
        summary="Revoke a durable consent record.",
        description="Administratively revokes a consent grant and returns the resulting persisted state.",
        params_model=ConsentRevokeParams,
        result_model=ConsentRevokeResult,
        handler=handle_consent_revoke,
        owner_module="tigrbl_auth/api/rpc/methods/consent.py",
        tags=("consent", "operator"),
    ),
)
