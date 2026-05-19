"""Directory-style operator/admin RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from tigrbl_auth.api.rpc.schemas.common import EmptyParams
from tigrbl_auth.api.rpc.schemas.directory import (
    ClientListParams,
    ClientListResult,
    ClientShowParams,
    ClientShowResult,
    IdentityListParams,
    IdentityListResult,
    IdentityShowParams,
    IdentityShowResult,
    TenantListParams,
    TenantListResult,
    TenantShowParams,
    TenantShowResult,
)
from tigrbl_auth.api.rpc.methods._shared import get_row, list_rows, row_to_dict


async def handle_tenant_list(params: TenantListParams, _context):
    from tigrbl_auth.tables import Tenant

    rows = await list_rows(Tenant, limit=params.limit, offset=params.offset, order_by="created_at")
    return TenantListResult(count=len(rows), items=[row_to_dict(row) for row in rows])


async def handle_tenant_show(params: TenantShowParams, _context):
    from tigrbl_auth.tables import Tenant

    row = await get_row(Tenant, id_value=params.id)
    return TenantShowResult(tenant=row_to_dict(row) if row else None)


async def handle_client_list(params: ClientListParams, _context):
    from tigrbl_auth.tables import Client

    rows = await list_rows(
        Client,
        filters={"tenant_id": params.tenant_id},
        limit=params.limit,
        offset=params.offset,
        order_by="created_at",
    )
    return ClientListResult(count=len(rows), items=[row_to_dict(row) for row in rows])


async def handle_client_show(params: ClientShowParams, _context):
    from tigrbl_auth.tables import Client

    row = await get_row(Client, id_value=params.id)
    return ClientShowResult(client=row_to_dict(row) if row else None)


async def handle_identity_list(params: IdentityListParams, _context):
    from tigrbl_auth.tables import User

    rows = await list_rows(
        User,
        filters={"tenant_id": params.tenant_id},
        limit=params.limit,
        offset=params.offset,
        order_by="created_at",
    )
    return IdentityListResult(count=len(rows), items=[row_to_dict(row) for row in rows])


async def handle_identity_show(params: IdentityShowParams, _context):
    from tigrbl_auth.tables import User

    row = await get_row(User, id_value=params.id)
    return IdentityShowResult(identity=row_to_dict(row) if row else None)


METHODS = (
    RpcMethodDefinition(
        name="tenant.list",
        summary="List tenants in the admin plane.",
        description="Returns tenant records from the durable admin control plane.",
        params_model=TenantListParams,
        result_model=TenantListResult,
        handler=handle_tenant_list,
        owner_module="tigrbl_auth/api/rpc/methods/directory.py",
        tags=("directory", "tenant"),
    ),
    RpcMethodDefinition(
        name="tenant.show",
        summary="Show a tenant in the admin plane.",
        description="Returns a single tenant record by identifier.",
        params_model=TenantShowParams,
        result_model=TenantShowResult,
        handler=handle_tenant_show,
        owner_module="tigrbl_auth/api/rpc/methods/directory.py",
        tags=("directory", "tenant"),
    ),
    RpcMethodDefinition(
        name="client.list",
        summary="List OAuth/OIDC clients in the admin plane.",
        description="Returns client rows from the admin control plane.",
        params_model=ClientListParams,
        result_model=ClientListResult,
        handler=handle_client_list,
        owner_module="tigrbl_auth/api/rpc/methods/directory.py",
        tags=("directory", "client"),
    ),
    RpcMethodDefinition(
        name="client.show",
        summary="Show a client in the admin plane.",
        description="Returns a single client record by identifier.",
        params_model=ClientShowParams,
        result_model=ClientShowResult,
        handler=handle_client_show,
        owner_module="tigrbl_auth/api/rpc/methods/directory.py",
        tags=("directory", "client"),
    ),
    RpcMethodDefinition(
        name="identity.list",
        summary="List identities in the admin plane.",
        description="Returns user/identity rows from the admin control plane.",
        params_model=IdentityListParams,
        result_model=IdentityListResult,
        handler=handle_identity_list,
        owner_module="tigrbl_auth/api/rpc/methods/directory.py",
        tags=("directory", "identity"),
    ),
    RpcMethodDefinition(
        name="identity.show",
        summary="Show an identity in the admin plane.",
        description="Returns a single user/identity record by identifier.",
        params_model=IdentityShowParams,
        result_model=IdentityShowResult,
        handler=handle_identity_show,
        owner_module="tigrbl_auth/api/rpc/methods/directory.py",
        tags=("directory", "identity"),
    ),
)
