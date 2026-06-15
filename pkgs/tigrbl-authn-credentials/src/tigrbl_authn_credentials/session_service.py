from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from ._operator_store import OperationContext, TransactionResult, utc_now
from .audit_service import record_surface_event
from .operator_service import (
    exchange_token,
    get_record,
    get_resource,
    introspect_token_record,
    list_resource_result,
    revoke_resource,
)


def token_hash(token: str) -> str:
    return hashlib.sha256(str(token).encode("utf-8")).hexdigest()


def _normalized_context(repo_root: Path, *, command: str, resource: str, actor: str | None = None, tenant: str | None = None, issuer: str | None = None, profile: str | None = None, dry_run: bool = False) -> OperationContext:
    return OperationContext(repo_root=repo_root, command=command, resource=resource, dry_run=dry_run, actor=actor or "system", tenant=tenant, issuer=issuer, profile=profile)


def list_sessions_for_context(context: OperationContext, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50) -> TransactionResult:
    return list_resource_result(context, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit)


def get_session_for_context(context: OperationContext, *, record_id: str) -> TransactionResult:
    return get_resource(context, record_id=record_id)


def revoke_session_for_context(context: OperationContext, *, record_id: str) -> TransactionResult:
    return revoke_resource(context, record_id=record_id)


def revoke_all_sessions_for_context(context: OperationContext, *, status_filter: str | None = None, filter_expr: str | None = None) -> TransactionResult:
    return revoke_resource(context, all_records=True, status_filter=status_filter, filter_expr=filter_expr)


def list_tokens_for_context(context: OperationContext, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50) -> TransactionResult:
    return list_resource_result(context, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit)


def get_token_for_context(context: OperationContext, *, record_id: str) -> TransactionResult:
    return get_resource(context, record_id=record_id)


def introspect_token_for_context(context: OperationContext, *, record_id: str) -> TransactionResult:
    result = get_resource(context, record_id=record_id)
    if result.record is None:
        return result
    result.summary = introspect_token_record(result.record)
    return result


def revoke_token_for_context(context: OperationContext, *, record_id: str) -> TransactionResult:
    return revoke_resource(context, record_id=record_id)


def revoke_all_tokens_for_context(context: OperationContext, *, status_filter: str | None = None, filter_expr: str | None = None) -> TransactionResult:
    return revoke_resource(context, all_records=True, status_filter=status_filter, filter_expr=filter_expr)


def exchange_token_for_context(context: OperationContext, *, subject_token: str | None, requested_token_type: str | None = None, audience: str | None = None, resource: str | None = None, actor_token: str | None = None, extras: Mapping[str, Any] | None = None) -> TransactionResult:
    return exchange_token(context, subject_token=subject_token, requested_token_type=requested_token_type, audience=audience, resource=resource, actor_token=actor_token, extras=extras)


def _observe_token_like(repo_root: Path, *, token: str, kind: str, actor: str | None = None, tenant: str | None = None, issuer: str | None = None, details: Mapping[str, Any] | None = None) -> str:
    from .operator_service import create_resource

    details = dict(details or {})
    record_id = token_hash(token)
    context = _normalized_context(repo_root, command="observe", resource="token", actor=actor, tenant=tenant, issuer=issuer)
    patch = {
        "token_hash": record_id,
        "token_kind": kind,
        "token_type": details.get("token_type") or kind,
        "subject": details.get("subject") or details.get("sub"),
        "client_id": details.get("client_id"),
        "scope": details.get("scope"),
        "issuer": issuer or details.get("issuer"),
        "audience": details.get("audience") or details.get("aud"),
        "issued_at": details.get("issued_at") or utc_now(),
        "expires_at": details.get("expires_at"),
        "claims": details.get("claims"),
        "token": token,
    }
    create_resource(context, record_id=record_id, patch=patch, if_exists="update")
    record_surface_event(repo_root, event_type=f"observe_{kind}", target_type="token", target_id=record_id, outcome="ok", tenant_id=tenant, actor_user_id=actor, details=details, source_surface="runtime")
    return record_id


def observe_token_response(repo_root: Path, *, access_token: str | None = None, refresh_token: str | None = None, id_token: str | None = None, actor: str | None = None, tenant: str | None = None, issuer: str | None = None, details: Mapping[str, Any] | None = None) -> dict[str, Any]:
    observed: dict[str, Any] = {}
    if access_token:
        observed["access_token_id"] = _observe_token_like(repo_root, token=access_token, kind="access", actor=actor, tenant=tenant, issuer=issuer, details=details)
    if refresh_token:
        observed["refresh_token_id"] = _observe_token_like(repo_root, token=refresh_token, kind="refresh", actor=actor, tenant=tenant, issuer=issuer, details=details)
    if id_token:
        observed["id_token_id"] = _observe_token_like(repo_root, token=id_token, kind="id", actor=actor, tenant=tenant, issuer=issuer, details=details)
    return observed


def observe_logout_response(repo_root: Path, *, session_id: str | None, actor: str | None = None, tenant: str | None = None, details: Mapping[str, Any] | None = None) -> dict[str, Any]:
    record_surface_event(repo_root, event_type="logout", target_type="session", target_id=session_id, outcome="ok", tenant_id=tenant, actor_user_id=actor, details=details, source_surface="runtime")
    return {"session_id": session_id, "status": "ok"}


def observe_device_authorization_response(repo_root: Path, *, device_code: str | None, actor: str | None = None, tenant: str | None = None, details: Mapping[str, Any] | None = None) -> dict[str, Any]:
    target_id = token_hash(device_code) if device_code else None
    record_surface_event(repo_root, event_type="device_authorization", target_type="token", target_id=target_id, outcome="ok", tenant_id=tenant, actor_user_id=actor, details=details, source_surface="runtime")
    return {"device_code_id": target_id, "status": "ok"}


def observe_par_response(repo_root: Path, *, request_uri: str | None, actor: str | None = None, tenant: str | None = None, details: Mapping[str, Any] | None = None) -> dict[str, Any]:
    target_id = token_hash(request_uri) if request_uri else None
    record_surface_event(repo_root, event_type="par", target_type="pushed_authorization_request", target_id=target_id, outcome="ok", tenant_id=tenant, actor_user_id=actor, details=details, source_surface="runtime")
    return {"request_uri_id": target_id, "status": "ok"}


__all__ = [
    "exchange_token_for_context",
    "get_session_for_context",
    "get_token_for_context",
    "introspect_token_for_context",
    "list_sessions_for_context",
    "list_tokens_for_context",
    "observe_device_authorization_response",
    "observe_logout_response",
    "observe_par_response",
    "observe_token_response",
    "revoke_all_sessions_for_context",
    "revoke_all_tokens_for_context",
    "revoke_session_for_context",
    "revoke_token_for_context",
    "token_hash",
]
