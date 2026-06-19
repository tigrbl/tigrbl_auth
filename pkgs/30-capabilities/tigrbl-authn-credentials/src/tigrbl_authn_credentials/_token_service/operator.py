from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..session_service import (
    exchange_token_for_context,
    get_token_for_context,
    introspect_token_for_context,
    list_tokens_for_context,
    revoke_all_tokens_for_context,
    revoke_token_for_context,
)


def parse_token_patch(raw_patch: dict[str, Any] | None) -> dict[str, Any]:
    patch = dict(raw_patch or {})
    patch.setdefault("issued_at", patch.get("iat") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))
    if "token_type" not in patch and "typ" in patch:
        patch["token_type"] = patch["typ"]
    return patch


def list_operator_tokens_for_context(context, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50):
    return list_tokens_for_context(context, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit)


def get_operator_token_for_context(context, *, record_id: str):
    return get_token_for_context(context, record_id=record_id)


def introspect_operator_token_for_context(context, *, record_id: str):
    return introspect_token_for_context(context, record_id=record_id)


def revoke_operator_token_for_context(context, *, record_id: str):
    return revoke_token_for_context(context, record_id=record_id)


def revoke_all_operator_tokens_for_context(context, *, status_filter: str | None = None, filter_expr: str | None = None):
    return revoke_all_tokens_for_context(context, status_filter=status_filter, filter_expr=filter_expr)


def exchange_operator_token_for_context(context, *, subject_token: str | None, requested_token_type: str | None = None, audience: str | None = None, resource: str | None = None, actor_token: str | None = None, extras: dict[str, Any] | None = None):
    return exchange_token_for_context(context, subject_token=subject_token, requested_token_type=requested_token_type, audience=audience, resource=resource, actor_token=actor_token, extras=extras)
