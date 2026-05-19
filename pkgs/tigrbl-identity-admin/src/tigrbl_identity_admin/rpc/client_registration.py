"""Dynamic client-registration management RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from tigrbl_auth.api.rpc.schemas.client_registration import (
    ClientRegistrationDeleteParams,
    ClientRegistrationDeleteResult,
    ClientRegistrationListParams,
    ClientRegistrationListResult,
    ClientRegistrationRecord,
    ClientRegistrationShowParams,
    ClientRegistrationShowResult,
    ClientRegistrationUpsertParams,
    ClientRegistrationUpsertResult,
)
from tigrbl_auth.api.rpc.methods._shared import repo_root_from_context
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.operator_service import create_resource, delete_resource, get_record, list_resource, update_resource


def _rpc_context(context, command: str) -> OperationContext:
    issuer = getattr(getattr(context, 'deployment', None), 'issuer', None)
    return OperationContext(repo_root=repo_root_from_context(context), command=command, resource='client', actor='rpc', profile=getattr(context, 'profile', None), issuer=issuer)


def _to_registration_record(record: dict | None) -> ClientRegistrationRecord | None:
    if record is None:
        return None
    data = record.get('data') or {}
    return ClientRegistrationRecord(
        id=str(record.get('id')),
        client_id=str(data.get('client_id') or record.get('id')),
        tenant_id=data.get('tenant_id') or record.get('tenant'),
        software_id=data.get('software_id'),
        software_version=data.get('software_version'),
        contacts=list(data.get('contacts') or []),
        registration_client_uri=data.get('registration_client_uri'),
        registration_access_token_hash=data.get('registration_access_token_hash'),
        issued_at=record.get('created_at'),
        rotated_at=data.get('rotated_at') or data.get('client_secret_rotated_at'),
        disabled_at=data.get('disabled_at'),
        registration_metadata=dict(data.get('metadata') or data.get('registration_metadata') or {}),
    )


async def handle_registration_list(params: ClientRegistrationListParams, context):
    items = list_resource(
        repo_root_from_context(context),
        'client',
        filter_expr=params.client_id or params.tenant_id,
        offset=params.offset,
        limit=params.limit,
        sort='id',
    )
    if params.client_id:
        items = [item for item in items if str((item.get('data') or {}).get('client_id') or item.get('id')) == params.client_id]
    if params.tenant_id:
        items = [item for item in items if str((item.get('data') or {}).get('tenant_id') or item.get('tenant')) == params.tenant_id]
    return ClientRegistrationListResult(count=len(items), items=[_to_registration_record(item) for item in items if _to_registration_record(item) is not None])


async def handle_registration_show(params: ClientRegistrationShowParams, context):
    row = get_record(repo_root_from_context(context), 'client', params.client_id)
    if row is None:
        items = list_resource(repo_root_from_context(context), 'client', filter_expr=params.client_id, offset=0, limit=100)
        for item in items:
            if str((item.get('data') or {}).get('client_id') or item.get('id')) == params.client_id:
                row = item
                break
    return ClientRegistrationShowResult(registration=_to_registration_record(row))


async def handle_registration_upsert(params: ClientRegistrationUpsertParams, context):
    patch = {
        'client_id': params.client_id,
        'tenant_id': params.tenant_id,
        'metadata': dict(params.metadata),
        'contacts': list(params.contacts),
        'software_id': params.software_id,
        'software_version': params.software_version,
        'registration_access_token_hash': params.registration_access_token_hash,
        'registration_client_uri': params.registration_client_uri,
    }
    existing = get_record(repo_root_from_context(context), 'client', params.client_id)
    if existing is None:
        result = create_resource(_rpc_context(context, 'client.registration.upsert'), record_id=params.client_id, patch=patch, if_exists='update')
        row = result.record
    else:
        result = update_resource(_rpc_context(context, 'client.registration.upsert'), record_id=params.client_id, patch=patch, if_missing='create')
        row = result.record
    return ClientRegistrationUpsertResult(registration=_to_registration_record(row))


async def handle_registration_delete(params: ClientRegistrationDeleteParams, context):
    result = delete_resource(_rpc_context(context, 'client.registration.delete'), record_id=params.client_id, if_missing='skip' if params.if_missing == 'skip' else 'error')
    deleted = result.record or {'id': params.client_id, 'data': {'client_id': params.client_id}}
    return ClientRegistrationDeleteResult(
        deleted=params.if_missing == 'skip' or result.status == 'deleted',
        registration=_to_registration_record(deleted),
        status=result.status,
    )


METHODS = (
    RpcMethodDefinition(
        name='client.registration.list',
        summary='List durable client-registration records.',
        description='Returns RFC 7591/7592 registration state from the shared operator service layer.',
        params_model=ClientRegistrationListParams,
        result_model=ClientRegistrationListResult,
        handler=handle_registration_list,
        owner_module='tigrbl_auth/api/rpc/methods/client_registration.py',
        tags=('client', 'registration', 'rfc7591', 'rfc7592'),
    ),
    RpcMethodDefinition(
        name='client.registration.show',
        summary='Show a durable client-registration record.',
        description='Returns a single registration record from the shared operator service layer.',
        params_model=ClientRegistrationShowParams,
        result_model=ClientRegistrationShowResult,
        handler=handle_registration_show,
        owner_module='tigrbl_auth/api/rpc/methods/client_registration.py',
        tags=('client', 'registration', 'rfc7591', 'rfc7592'),
    ),
    RpcMethodDefinition(
        name='client.registration.upsert',
        summary='Create or update a durable client-registration record.',
        description='Persists registration state through the same service layer used by the CLI surface.',
        params_model=ClientRegistrationUpsertParams,
        result_model=ClientRegistrationUpsertResult,
        handler=handle_registration_upsert,
        owner_module='tigrbl_auth/api/rpc/methods/client_registration.py',
        tags=('client', 'registration', 'rfc7591', 'rfc7592'),
    ),
    RpcMethodDefinition(
        name='client.registration.delete',
        summary='Delete a durable client-registration record.',
        description='Deletes RFC 7592 registration state through the shared operator service layer.',
        params_model=ClientRegistrationDeleteParams,
        result_model=ClientRegistrationDeleteResult,
        handler=handle_registration_delete,
        owner_module='tigrbl_auth/api/rpc/methods/client_registration.py',
        tags=('client', 'registration', 'rfc7592'),
    ),
)
