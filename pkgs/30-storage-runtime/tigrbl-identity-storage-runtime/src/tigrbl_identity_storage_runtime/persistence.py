"""Compatibility surface for lifecycle helpers now owned by layer 30."""

from __future__ import annotations

import warnings
from typing import Any

from tigrbl_identity_core.digests import token_hash
from tigrbl_identity_storage.tables._sync import run_async

from .consent_lifecycle import (
    record_consent,
    record_consent_async,
    revoke_consent,
    revoke_consent_async,
)
from .oidc_persistence import (
    get_latest_logout_for_session_async,
    mark_logout_channel_async,
    terminate_session_async,
    update_logout_metadata_async,
)
from .ops.oauth_state import record_revoked_token_hash
from .registration_lifecycle import (
    get_client_registration,
    get_client_registration_async,
    upsert_client_registration,
    upsert_client_registration_async,
)
from .session_lifecycle import (
    bind_session_client_async,
    create_session_async,
    get_active_session_async,
    get_session_async,
    rotate_session_cookie_secret_async,
    touch_session_async,
)
from .token_lifecycle import (
    introspect_token,
    introspect_token_async,
    is_revoked,
    is_revoked_async,
    is_token_revoked,
    is_token_revoked_async,
    reset_revocations,
    reset_revocations_async,
    reset_token_state,
    reset_token_state_async,
    revoke_token,
    revoke_token_async,
    upsert_token_record,
    upsert_token_record_async,
)
from .token_persistence import (
    get_token_record_async,
    mark_token_used_async,
    remove_token_record_async,
    revoke_refresh_family_async,
)

warnings.warn(
    "tigrbl_auth.services.persistence is deprecated; import lifecycle adapters "
    "from tigrbl_identity_storage_runtime instead.",
    DeprecationWarning,
    stacklevel=2,
)


def bind_session_client(session_id: Any, **kwargs: Any):
    return run_async(bind_session_client_async(session_id, **kwargs))


def create_session(**kwargs: Any):
    return run_async(create_session_async(**kwargs))


def get_active_session(session_id: Any):
    return run_async(get_active_session_async(session_id))


def get_session(session_id: Any):
    return run_async(get_session_async(session_id))


def rotate_session_cookie_secret(session_id: Any, **kwargs: Any):
    return run_async(rotate_session_cookie_secret_async(session_id, **kwargs))


def touch_session(session_id: Any):
    return run_async(touch_session_async(session_id))


def get_latest_logout_for_session(session_id: Any):
    return run_async(get_latest_logout_for_session_async(session_id))


def mark_logout_channel(logout_id: Any, **kwargs: Any):
    return run_async(mark_logout_channel_async(logout_id, **kwargs))


def terminate_session(session_id: Any, **kwargs: Any):
    return run_async(terminate_session_async(session_id, **kwargs))


def update_logout_metadata(logout_id: Any, **kwargs: Any):
    return run_async(update_logout_metadata_async(logout_id, **kwargs))


async def persist_revoked_token_hash(db: Any, **kwargs: Any):
    return await record_revoked_token_hash({"payload": kwargs, "db": db})


def get_token_record(token: str):
    return run_async(get_token_record_async(token))


def mark_token_used(token: str, **kwargs: Any):
    return run_async(mark_token_used_async(token, **kwargs))


def revoke_refresh_family(family_id: str, **kwargs: Any):
    return run_async(revoke_refresh_family_async(family_id, **kwargs))


def unregister_token(token: str):
    return run_async(remove_token_record_async(token))


record_token = upsert_token_record


__all__ = [
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
    "is_revoked",
    "is_revoked_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "mark_logout_channel",
    "mark_logout_channel_async",
    "mark_token_used",
    "mark_token_used_async",
    "persist_revoked_token_hash",
    "record_consent",
    "record_consent_async",
    "record_token",
    "remove_token_record_async",
    "reset_revocations",
    "reset_revocations_async",
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
