"""Token inspection RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from tigrbl_auth.api.rpc.schemas.token import (
    TokenExchangeParams,
    TokenExchangeResult,
    TokenInspectParams,
    TokenInspectResult,
    TokenListParams,
    TokenListResult,
    TokenRecordView,
)
from tigrbl_auth.api.rpc.methods._shared import repo_root_from_context
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.session_service import token_hash
from tigrbl_auth.services.token_service import (
    exchange_operator_token_for_context,
    introspect_operator_token_for_context,
    list_operator_tokens_for_context,
)


def _rpc_context(context, command: str) -> OperationContext:
    issuer = getattr(getattr(context, 'deployment', None), 'issuer', None)
    return OperationContext(repo_root=repo_root_from_context(context), command=command, resource='token', actor='rpc', profile=getattr(context, 'profile', None), issuer=issuer)


def _to_token_view(record: dict | None) -> TokenRecordView | None:
    if record is None:
        return None
    data = record.get('data') or {}
    return TokenRecordView(
        id=str(record.get('id')) if record.get('id') is not None else None,
        token_hash=data.get('token_hash') or str(record.get('id')),
        token_kind=data.get('token_kind'),
        token_type_hint=data.get('token_type') or data.get('token_type_hint'),
        active=record.get('status') not in {'revoked', 'retired', 'deleted'},
        subject=data.get('subject') or data.get('sub'),
        tenant_id=data.get('tenant_id') or record.get('tenant'),
        client_id=data.get('client_id'),
        scope=data.get('scope'),
        issuer=data.get('issuer') or data.get('iss'),
        audience=data.get('audience') or data.get('aud'),
        issued_at=data.get('issued_at'),
        expires_at=data.get('expires_at'),
        revoked_at=data.get('revoked_at'),
        revoked_reason=data.get('revoked_reason'),
        claims=dict(data.get('claims') or {}),
    )


async def handle_token_list(params: TokenListParams, context):
    result = list_operator_tokens_for_context(_rpc_context(context, 'token.list'), status_filter='active' if params.active_only else None, filter_expr=params.subject or params.client_id, offset=params.offset, limit=params.limit, sort='id')
    items = []
    for item in result.items or []:
        data = item.get('data') or {}
        if params.subject and str(data.get('subject') or data.get('sub')) != str(params.subject):
            continue
        if params.client_id and str(data.get('client_id')) != str(params.client_id):
            continue
        mapped = _to_token_view(item)
        if mapped is not None:
            items.append(mapped)
    return TokenListResult(count=len(items), items=items)


async def handle_token_inspect(params: TokenInspectParams, context):
    record_id = token_hash(params.token)
    result = introspect_operator_token_for_context(_rpc_context(context, 'token.inspect'), record_id=record_id)
    introspection = dict(result.summary or {})
    return TokenInspectResult(token_hash=record_id, active=bool(introspection.get('active', False)), revoked=not bool(introspection.get('active', False)), introspection=introspection)


async def handle_token_exchange(params: TokenExchangeParams, context):
    result = exchange_operator_token_for_context(
        _rpc_context(context, 'token.exchange'),
        subject_token=params.subject_token,
        requested_token_type=params.requested_token_type,
        audience=params.audience,
        resource=params.resource,
        actor_token=params.actor_token,
        extras=dict(params.extras),
    )
    return TokenExchangeResult(status=result.status, token=_to_token_view(result.record))


METHODS = (
    RpcMethodDefinition(
        name='token.list',
        summary='List durable token records.',
        description='Returns token status records from the shared operator service layer.',
        params_model=TokenListParams,
        result_model=TokenListResult,
        handler=handle_token_list,
        owner_module='tigrbl_auth/api/rpc/methods/token.py',
        tags=('token', 'rfc7662'),
    ),
    RpcMethodDefinition(
        name='token.inspect',
        summary='Inspect token posture and current introspection state.',
        description='Returns token hash, active state, revocation state, and the introspection payload.',
        params_model=TokenInspectParams,
        result_model=TokenInspectResult,
        handler=handle_token_inspect,
        owner_module='tigrbl_auth/api/rpc/methods/token.py',
        tags=('token', 'rfc7662', 'rfc7009'),
    ),
    RpcMethodDefinition(
        name='token.exchange',
        summary='Create a durable token exchange record.',
        description='Persists RFC 8693 token-exchange lineage through the shared operator service layer.',
        params_model=TokenExchangeParams,
        result_model=TokenExchangeResult,
        handler=handle_token_exchange,
        owner_module='tigrbl_auth/api/rpc/methods/token.py',
        tags=('token', 'rfc8693'),
    ),
)
