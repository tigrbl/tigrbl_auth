"""Session inspection and termination RPC methods."""

from __future__ import annotations

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition
from tigrbl_auth.api.rpc.schemas.session import (
    SessionListParams,
    SessionListResult,
    SessionRecord,
    SessionShowParams,
    SessionShowResult,
    SessionTerminateParams,
    SessionTerminateResult,
)
from tigrbl_auth.api.rpc.methods._shared import repo_root_from_context
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.audit_service import latest_audit_event
from tigrbl_auth.services.session_service import (
    get_session_for_context,
    list_sessions_for_context,
    revoke_session_for_context,
)


def _rpc_context(context, command: str) -> OperationContext:
    issuer = getattr(getattr(context, 'deployment', None), 'issuer', None)
    return OperationContext(repo_root=repo_root_from_context(context), command=command, resource='session', actor='rpc', profile=getattr(context, 'profile', None), issuer=issuer)


def _to_session_record(record: dict | None) -> SessionRecord | None:
    if record is None:
        return None
    data = record.get('data') or {}
    return SessionRecord(
        id=str(record.get('id')),
        user_id=data.get('user_id'),
        tenant_id=data.get('tenant_id') or record.get('tenant'),
        username=data.get('username'),
        client_id=data.get('client_id'),
        auth_time=data.get('auth_time') or record.get('created_at'),
        session_state=data.get('session_state'),
        expires_at=data.get('expires_at'),
        last_seen_at=data.get('last_seen_at') or record.get('updated_at'),
        ended_at=data.get('ended_at') or data.get('revoked_at'),
        logout_reason=data.get('logout_reason'),
        metadata=dict(data.get('metadata') or {}),
    )


async def handle_session_list(params: SessionListParams, context):
    result = list_sessions_for_context(
        _rpc_context(context, 'session.list'),
        status_filter='active' if params.active_only else None,
        filter_expr=params.user_id or params.client_id or params.tenant_id,
        offset=params.offset,
        limit=params.limit,
        sort='id',
    )
    items = []
    for item in result.items or []:
        data = item.get('data') or {}
        if params.user_id and str(data.get('user_id')) != str(params.user_id):
            continue
        if params.client_id and str(data.get('client_id')) != str(params.client_id):
            continue
        if params.tenant_id and str(data.get('tenant_id') or item.get('tenant')) != str(params.tenant_id):
            continue
        mapped = _to_session_record(item)
        if mapped is not None:
            items.append(mapped)
    return SessionListResult(count=len(items), items=items)


async def handle_session_show(params: SessionShowParams, context):
    result = get_session_for_context(_rpc_context(context, 'session.show'), record_id=params.session_id)
    latest_logout = latest_audit_event(repo_root_from_context(context), target_type='session')
    return SessionShowResult(session=_to_session_record(result.record), latest_logout=latest_logout)


async def handle_session_terminate(params: SessionTerminateParams, context):
    result = revoke_session_for_context(_rpc_context(context, 'session.terminate'), record_id=params.session_id)
    return SessionTerminateResult(session=_to_session_record((result.items or [None])[0] if result.items else result.record), logout_state={'initiated_by': params.initiated_by, 'reason': params.reason, 'frontchannel_required': params.frontchannel_required, 'backchannel_required': params.backchannel_required, 'metadata': dict(params.metadata)})


METHODS = (
    RpcMethodDefinition(
        name='session.list',
        summary='List durable browser and auth sessions.',
        description='Returns session records from the shared operator service layer.',
        params_model=SessionListParams,
        result_model=SessionListResult,
        handler=handle_session_list,
        owner_module='tigrbl_auth/api/rpc/methods/session.py',
        tags=('session', 'oidc'),
    ),
    RpcMethodDefinition(
        name='session.show',
        summary='Show a durable session and its latest logout state.',
        description='Returns a single session together with its latest logout propagation state.',
        params_model=SessionShowParams,
        result_model=SessionShowResult,
        handler=handle_session_show,
        owner_module='tigrbl_auth/api/rpc/methods/session.py',
        tags=('session', 'oidc'),
    ),
    RpcMethodDefinition(
        name='session.terminate',
        summary='Terminate a durable session and persist logout state.',
        description='Administratively ends a session through the same service layer used by the CLI surface.',
        params_model=SessionTerminateParams,
        result_model=SessionTerminateResult,
        handler=handle_session_terminate,
        owner_module='tigrbl_auth/api/rpc/methods/session.py',
        tags=('session', 'logout', 'oidc'),
    ),
)
