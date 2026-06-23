"""Deprecated compatibility facade for table-owned storage lifecycle helpers."""

from __future__ import annotations

import warnings
from tigrbl_identity_storage.tables._ops import token_hash
from tigrbl_identity_storage.tables.audit_event import append_audit_event, append_audit_event_async
from tigrbl_identity_storage.tables.auth_session._lifecycle import (
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
from tigrbl_identity_storage.tables.client_registration._lifecycle import (
    get_client_registration,
    get_client_registration_async,
    upsert_client_registration,
    upsert_client_registration_async,
)
from tigrbl_identity_storage.tables.consent._lifecycle import (
    record_consent,
    record_consent_async,
    revoke_consent,
    revoke_consent_async,
)
from tigrbl_identity_storage.tables.logout_state._lifecycle import (
    get_latest_logout_for_session,
    get_latest_logout_for_session_async,
    mark_logout_channel,
    mark_logout_channel_async,
    terminate_session,
    terminate_session_async,
    update_logout_metadata,
    update_logout_metadata_async,
)
from tigrbl_identity_storage.tables.revoked_token._op import (
    is_token_revoked,
    is_token_revoked_async,
    reset_token_state,
    reset_token_state_async,
    revoke_token,
    revoke_token_async,
)
from tigrbl_identity_storage.tables.token_record._introspection_store import (
    introspect_token_record_async as introspect_token_async,
)
from tigrbl_identity_storage.tables.token_record._lifecycle import (
    get_token_record_async,
    mark_token_used_async,
    remove_token_record_async,
    revoke_refresh_family_async,
    upsert_token_record_async,
)
from tigrbl_identity_storage.tables._sync import run_async

warnings.warn(
    "tigrbl_identity_storage.persistence is deprecated; import lifecycle helpers from "
    "tigrbl_identity_storage.tables.<table> modules instead.",
    DeprecationWarning,
    stacklevel=2,
)

record_token = upsert_token_record = lambda token, claims=None, token_kind=None, token_type_hint=None: run_async(
    upsert_token_record_async(token, claims, token_kind=token_kind, token_type_hint=token_type_hint)
)
get_token_record = lambda token: run_async(get_token_record_async(token))
unregister_token = lambda token: run_async(remove_token_record_async(token))
mark_token_used = lambda token, successor_token=None, reason="refresh_rotated": run_async(
    mark_token_used_async(token, successor_token=successor_token, reason=reason)
)
revoke_refresh_family = lambda family_id, reason="refresh_token_reuse_detected", reuse_token=None: run_async(
    revoke_refresh_family_async(family_id, reason=reason, reuse_token=reuse_token)
)
introspect_token = lambda token: run_async(introspect_token_async(token))


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
