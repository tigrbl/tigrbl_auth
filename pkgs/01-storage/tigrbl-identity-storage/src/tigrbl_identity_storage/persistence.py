"""Deprecated compatibility facade for table-owned storage lifecycle helpers."""

from __future__ import annotations

import warnings
from tigrbl_identity_storage.tables._ops import token_hash
from tigrbl_identity_storage.tables.audit_event import append_audit_event, append_audit_event_async
from tigrbl_identity_storage.tables.auth_session._ops import (
    bind_session_client,
    bind_session_client_async,
    create_session,
    create_session_async,
    get_active_session,
    get_active_session_async,
    get_session,
    get_session_async,
    rotate_session_cookie_secret,
    rotate_session_cookie_secret_async,
    touch_session,
    touch_session_async,
)
from tigrbl_identity_storage.tables.consent._ops import (
    record_consent,
    record_consent_async,
    revoke_consent,
    revoke_consent_async,
)
from tigrbl_identity_storage.tables.revoked_token._ops import (
    is_token_revoked,
    is_token_revoked_async,
    reset_token_state,
    reset_token_state_async,
    revoke_token,
    revoke_token_async,
)
from tigrbl_identity_storage.tables.token_record._ops import (
    introspect_token_record_async as introspect_token_async,
)
from tigrbl_identity_storage.tables.token_record._ops import (
    get_token_record_async,
    mark_token_used_async,
    remove_token_record_async,
    revoke_refresh_family_async,
    upsert_token_record_async,
)
from tigrbl_identity_storage.tables._sync import run_async
from tigrbl_identity_storage.tables.auth_session import AuthSession
from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage.tables.engine import storage_session
from tigrbl_identity_storage.tables.logout_state import LogoutState

warnings.warn(
    "tigrbl_identity_storage.persistence is deprecated; import lifecycle helpers from "
    "tigrbl_identity_storage.tables.<table> modules instead.",
    DeprecationWarning,
    stacklevel=2,
)


def _items(result):
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [] if result is None else [result]


async def get_client_registration_async(client_id):
    async with storage_session() as db:
        result = await ClientRegistration.handlers.list.core(
            {"payload": {"filters": {"client_id": client_id}}, "db": db}
        )
    rows = _items(result)
    return rows[0] if rows else None


async def upsert_client_registration_async(**kwargs):
    async with storage_session() as db:
        return await ClientRegistration.handlers.upsert.core({"payload": kwargs, "db": db})


def get_client_registration(client_id):
    return run_async(get_client_registration_async(client_id))


def upsert_client_registration(**kwargs):
    return run_async(upsert_client_registration_async(**kwargs))


async def terminate_session_async(session_id, **kwargs):
    async with storage_session() as db:
        session = await AuthSession.handlers.terminate.core({"path_params": {"id": session_id}, "payload": kwargs, "db": db})
        if session is None:
            return None
        return await LogoutState.handlers.ensure_for_session.core({"payload": {"session_id": session_id, **kwargs}, "db": db})


async def mark_logout_channel_async(logout_id, **kwargs):
    async with storage_session() as db:
        return await LogoutState.handlers.mark_channel.core(
            {"path_params": {"id": logout_id}, "payload": {"logout_id": logout_id, **kwargs}, "db": db}
        )


async def get_latest_logout_for_session_async(session_id):
    async with storage_session() as db:
        return await LogoutState.handlers.latest_for_session.core({"payload": {"session_id": session_id}, "db": db})


async def update_logout_metadata_async(logout_id, **kwargs):
    async with storage_session() as db:
        return await LogoutState.handlers.update_metadata.core(
            {"path_params": {"id": logout_id}, "payload": {"logout_id": logout_id, **kwargs}, "db": db}
        )


def terminate_session(session_id, **kwargs):
    return run_async(terminate_session_async(session_id, **kwargs))


def mark_logout_channel(logout_id, **kwargs):
    return run_async(mark_logout_channel_async(logout_id, **kwargs))


def get_latest_logout_for_session(session_id):
    return run_async(get_latest_logout_for_session_async(session_id))


def update_logout_metadata(logout_id, **kwargs):
    return run_async(update_logout_metadata_async(logout_id, **kwargs))


record_token = upsert_token_record = lambda token, claims=None, token_kind=None, token_type_hint=None: run_async(
    upsert_token_record_async(token, claims, token_kind=token_kind, token_type_hint=token_type_hint)
)
def get_token_record(token):
    return run_async(get_token_record_async(token))
def unregister_token(token):
    return run_async(remove_token_record_async(token))
def mark_token_used(token, successor_token=None, reason="refresh_rotated"):
    return run_async(
    mark_token_used_async(token, successor_token=successor_token, reason=reason)
)
def revoke_refresh_family(family_id, reason="refresh_token_reuse_detected", reuse_token=None):
    return run_async(
    revoke_refresh_family_async(family_id, reason=reason, reuse_token=reuse_token)
)
def introspect_token(token):
    return run_async(introspect_token_async(token))


__all__ = [
    "append_audit_event",
    "append_audit_event_async",
    "bind_session_client",
    "bind_session_client_async",
    "create_session",
    "create_session_async",
    "get_active_session",
    "get_active_session_async",
    "get_client_registration",
    "get_client_registration_async",
    "get_latest_logout_for_session",
    "get_latest_logout_for_session_async",
    "get_session",
    "get_session_async",
    "get_token_record",
    "get_token_record_async",
    "introspect_token",
    "introspect_token_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "mark_logout_channel",
    "mark_logout_channel_async",
    "mark_token_used",
    "mark_token_used_async",
    "record_consent",
    "record_consent_async",
    "record_token",
    "reset_token_state",
    "reset_token_state_async",
    "revoke_consent",
    "revoke_consent_async",
    "revoke_refresh_family",
    "revoke_refresh_family_async",
    "revoke_token",
    "revoke_token_async",
    "rotate_session_cookie_secret",
    "rotate_session_cookie_secret_async",
    "terminate_session",
    "terminate_session_async",
    "token_hash",
    "touch_session",
    "touch_session_async",
    "unregister_token",
    "update_logout_metadata",
    "update_logout_metadata_async",
    "upsert_client_registration",
    "upsert_client_registration_async",
    "upsert_token_record",
    "upsert_token_record_async",
]
