"""Key- and JWKS-oriented RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from typing import Any

from tigrbl_auth.api.rpc.schemas.keys import (
    JwksShowParams,
    JwksShowResult,
    KeyRecord,
    KeysListParams,
    KeysListResult,
    KeysRotateParams,
    KeysRotateResult,
    TenantKeyCreateParams,
    TenantKeyDeleteParams,
    TenantKeyMutationResult,
    TenantKeySeedParams,
    TenantKeyUpdateParams,
)
from tigrbl_auth.api.rpc.methods._shared import repo_root_from_context
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.audit_service import list_audit_events
from tigrbl_auth.services.key_management import (
    delete_operator_key_for_context,
    generate_operator_key_for_context,
    list_operator_keys_for_context,
    publish_operator_jwks_for_context,
    rotate_operator_key_for_context,
)
from tigrbl_auth.services.operator_service import create_resource, key_is_publicly_publishable, update_resource


def _rpc_context(context, command: str, *, tenant: str | None = None) -> OperationContext:
    issuer = getattr(getattr(context, 'deployment', None), 'issuer', None)
    return OperationContext(repo_root=repo_root_from_context(context), command=command, resource='keys', actor='rpc', profile=getattr(context, 'profile', None), tenant=tenant, issuer=issuer)


def _to_key_record(record: dict) -> KeyRecord:
    data = record.get('data') or {}
    tenant = record.get('tenant')
    return KeyRecord(
        id=str(record.get('id')),
        kind='operator-key',
        kid=data.get('kid') or str(record.get('id')),
        label=data.get('label'),
        service_id=data.get('service_id'),
        digest=data.get('digest'),
        created_at=record.get('created_at'),
        valid_from=data.get('valid_from'),
        valid_to=data.get('valid_to'),
        metadata={**dict(data), 'tenant': tenant, 'tenant_slug': tenant},
    )


def _tenant(params: Any) -> str:
    value = getattr(params, 'tenant', None) or getattr(params, 'tenant_id', None)
    if not value:
        raise ValueError('tenant is required')
    return str(value)


def _mutation_patch(params: Any, *, include_defaults: bool) -> dict[str, Any]:
    fields = ('kid', 'label', 'status', 'alg', 'kty', 'use', 'crv', 'x', 'n', 'e', 'publish')
    patch: dict[str, Any] = {}
    for field in fields:
        value = getattr(params, field, None)
        if include_defaults or value is not None:
            if value is not None:
                patch[field] = value
    if 'crv' in patch:
        patch['curve'] = patch['crv']
    return patch


def _jwks_for_context(context: OperationContext) -> dict[str, Any]:
    artifact = publish_operator_jwks_for_context(context)
    import json
    jwks_path = context.repo_root / artifact.path
    return json.loads(jwks_path.read_text(encoding='utf-8')) if jwks_path.exists() else {'keys': []}


async def handle_keys_list(params: KeysListParams, context):
    tenant = params.tenant or params.tenant_id
    result = list_operator_keys_for_context(_rpc_context(context, 'keys.list', tenant=tenant), limit=100, offset=0)
    rows = [_to_key_record(item) for item in (result.items or [])]
    rotation_events = [item for item in list_audit_events(repo_root_from_context(context)) if item.get('target_type') == 'keys']
    return KeysListResult(key_count=len(rows), rotation_event_count=len(rotation_events), keys=rows, rotation_events=rotation_events)


async def handle_jwks_show(_params: JwksShowParams, context):
    artifact = publish_operator_jwks_for_context(_rpc_context(context, 'jwks.show'))
    jwks_path = repo_root_from_context(context) / artifact.path
    import json
    jwks = json.loads(jwks_path.read_text(encoding='utf-8')) if jwks_path.exists() else {'keys': []}
    return JwksShowResult(jwks=jwks)


async def handle_tenant_key_seed(params: TenantKeySeedParams, context):
    tenant = _tenant(params)
    ctx = _rpc_context(context, 'tenant.keys.seed', tenant=tenant)
    existing = list_operator_keys_for_context(ctx, limit=1000, offset=0).items or []
    publishable = [item for item in existing if key_is_publicly_publishable(item)]
    if publishable and not params.force:
        return TenantKeyMutationResult(status='exists', key=_to_key_record(publishable[0]), jwks=_jwks_for_context(ctx))
    patch = _mutation_patch(params, include_defaults=True)
    patch.setdefault('publish', True)
    patch['kid'] = patch.get('kid') or f'{tenant}-jwks-active'
    created = generate_operator_key_for_context(ctx, patch=patch)
    return TenantKeyMutationResult(status=created.status, key=_to_key_record(created.record or {}), jwks=_jwks_for_context(ctx))


async def handle_tenant_key_create(params: TenantKeyCreateParams, context):
    tenant = _tenant(params)
    ctx = _rpc_context(context, 'tenant.keys.create', tenant=tenant)
    created = create_resource(ctx, record_id=params.kid, patch=_mutation_patch(params, include_defaults=True), if_exists='error')
    return TenantKeyMutationResult(status=created.status, key=_to_key_record(created.record or {}), jwks=_jwks_for_context(ctx))


async def handle_tenant_key_update(params: TenantKeyUpdateParams, context):
    tenant = _tenant(params)
    ctx = _rpc_context(context, 'tenant.keys.update', tenant=tenant)
    updated = update_resource(ctx, record_id=params.kid, patch=_mutation_patch(params, include_defaults=False))
    return TenantKeyMutationResult(status=updated.status, key=_to_key_record(updated.record or {}), jwks=_jwks_for_context(ctx))


async def handle_tenant_key_delete(params: TenantKeyDeleteParams, context):
    tenant = _tenant(params)
    ctx = _rpc_context(context, 'tenant.keys.delete', tenant=tenant)
    deleted = delete_operator_key_for_context(ctx, record_id=params.kid)
    return TenantKeyMutationResult(status=deleted.status, key=_to_key_record(deleted.record or {}), jwks=_jwks_for_context(ctx))


async def handle_keys_rotate(params: KeysRotateParams, context):
    result = list_operator_keys_for_context(_rpc_context(context, 'keys.rotate.lookup'), limit=1, offset=0, sort='id')
    if not result.items:
        rotate_result = publish_operator_jwks_for_context(_rpc_context(context, 'jwks.bootstrap'))
        _ = rotate_result
        # no key to rotate; create a placeholder by publishing current state and report not-found
        from tigrbl_auth.services.key_management import generate_operator_key_for_context
        created = generate_operator_key_for_context(_rpc_context(context, 'keys.rotate.seed'), patch={'label': 'rpc-rotation-seed', 'status': 'active', 'enabled': True})
        target_id = created.record['id']
    else:
        target_id = str(result.items[0]['id'])
    rotate = rotate_operator_key_for_context(_rpc_context(context, 'keys.rotate'), record_id=target_id)
    return KeysRotateResult(status='rotated', new_kid=str((rotate.record or {}).get('id', target_id)), rotation_event={'reason': params.reason, 'result': rotate.to_payload()})


METHODS = (
    RpcMethodDefinition(
        name='keys.list',
        summary='List durable service keys and key-rotation history.',
        description='Returns key rows and key-rotation audit rows from the shared operator service layer.',
        params_model=KeysListParams,
        result_model=KeysListResult,
        handler=handle_keys_list,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('keys', 'jwks'),
    ),
    RpcMethodDefinition(
        name='jwks.show',
        summary='Show the effective JWKS document.',
        description='Returns the effective JWKS publication payload generated by the shared service layer.',
        params_model=JwksShowParams,
        result_model=JwksShowResult,
        handler=handle_jwks_show,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('keys', 'jwks'),
    ),
    RpcMethodDefinition(
        name='keys.rotate',
        summary='Rotate the signing key and persist a key-rotation event.',
        description='Performs an operator key rotation through the same service layer used by the CLI surface.',
        params_model=KeysRotateParams,
        result_model=KeysRotateResult,
        handler=handle_keys_rotate,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('keys', 'jwks'),
    ),
    RpcMethodDefinition(
        name='tenant.keys.seed',
        summary='Seed a publishable tenant JWKS key.',
        description='Creates an active publishable tenant-scoped key when none exists, or reports the existing publishable key.',
        params_model=TenantKeySeedParams,
        result_model=TenantKeyMutationResult,
        handler=handle_tenant_key_seed,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('tenant', 'keys', 'jwks'),
    ),
    RpcMethodDefinition(
        name='tenant.keys.create',
        summary='Create a tenant JWKS key record.',
        description='Creates a tenant-scoped public JWKS key record through the durable operator-state service.',
        params_model=TenantKeyCreateParams,
        result_model=TenantKeyMutationResult,
        handler=handle_tenant_key_create,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('tenant', 'keys', 'jwks'),
    ),
    RpcMethodDefinition(
        name='tenant.keys.update',
        summary='Update a tenant JWKS key record.',
        description='Updates tenant-scoped key lifecycle and public JWK publication metadata.',
        params_model=TenantKeyUpdateParams,
        result_model=TenantKeyMutationResult,
        handler=handle_tenant_key_update,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('tenant', 'keys', 'jwks'),
    ),
    RpcMethodDefinition(
        name='tenant.keys.delete',
        summary='Delete a tenant JWKS key record.',
        description='Deletes a tenant-scoped key record from durable operator-state storage.',
        params_model=TenantKeyDeleteParams,
        result_model=TenantKeyMutationResult,
        handler=handle_tenant_key_delete,
        owner_module='tigrbl_auth/api/rpc/methods/keys.py',
        tags=('tenant', 'keys', 'jwks'),
    ),
)
