"""Durable OIDC session/logout operation composition owned by layer 30."""

from __future__ import annotations

from types import SimpleNamespace

from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage.tables.engine import storage_session

from .session_lifecycle import (
    bind_session_client_async,
    create_session_async,
    get_active_session_async,
    get_session_async,
    rotate_session_cookie_secret_async,
    touch_session_async,
)

from .ops.common import first_table_record
from .ops.oidc_logout import (
    ensure_logout_for_session,
    latest_logout_for_session,
    mark_logout_channel,
    update_logout_metadata,
)
from .ops.oidc_replay import register_backchannel_logout_replay
from .ops.sessions import terminate_session


async def get_client_registration_async(client_id):
    async with storage_session() as db:
        return await first_table_record(
            ClientRegistration, db, {"client_id": client_id}
        )


async def get_latest_logout_for_session_async(session_id):
    async with storage_session() as db:
        return await latest_logout_for_session(
            {"payload": {"session_id": session_id}, "db": db}
        )


async def terminate_session_async(session_id, **kwargs):
    async with storage_session() as db:
        session = await terminate_session(
            {"path_params": {"id": session_id}, "payload": kwargs, "db": db}
        )
        if session is None:
            return None
        return await ensure_logout_for_session(
            {"payload": {"session_id": session_id, **kwargs}, "db": db}
        )


async def update_logout_metadata_async(logout_id, **kwargs):
    async with storage_session() as db:
        return await update_logout_metadata(
            {
                "path_params": {"id": logout_id},
                "payload": {"logout_id": logout_id, **kwargs},
                "db": db,
            }
        )


async def mark_logout_channel_async(logout_id, **kwargs):
    async with storage_session() as db:
        return await mark_logout_channel(
            {
                "path_params": {"id": logout_id},
                "payload": {"logout_id": logout_id, **kwargs},
                "db": db,
            }
        )


async def register_backchannel_replay_async(*, jti, issuer, client_id, expires_at, now):
    async with storage_session() as db:
        return await register_backchannel_logout_replay(
            {
                "payload": {
                    "jti": jti,
                    "issuer": issuer,
                    "client_id": str(client_id),
                    "expires_at": expires_at,
                    "now": now,
                },
                "db": db,
            }
        )


oidc_persistence = SimpleNamespace(
    bind_session_client_async=bind_session_client_async,
    create_session_async=create_session_async,
    get_active_session_async=get_active_session_async,
    get_client_registration_async=get_client_registration_async,
    get_latest_logout_for_session_async=get_latest_logout_for_session_async,
    get_session_async=get_session_async,
    mark_logout_channel_async=mark_logout_channel_async,
    register_backchannel_replay_async=register_backchannel_replay_async,
    rotate_session_cookie_secret_async=rotate_session_cookie_secret_async,
    terminate_session_async=terminate_session_async,
    touch_session_async=touch_session_async,
    update_logout_metadata_async=update_logout_metadata_async,
)


__all__ = ["oidc_persistence"]
