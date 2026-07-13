"""Durable OIDC session/logout repository composition owned by layer 30."""

from __future__ import annotations

from types import SimpleNamespace

from tigrbl_identity_storage.persistence import (
    bind_session_client_async,
    create_session_async,
    get_active_session_async,
    get_session_async,
    rotate_session_cookie_secret_async,
    touch_session_async,
)
from tigrbl_identity_storage.tables.auth_session import AuthSession
from tigrbl_identity_storage.tables.backchannel_logout_replay import BackchannelLogoutReplay
from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage.tables.engine import storage_session
from tigrbl_identity_storage.tables.logout_state import LogoutState


def _items(result):
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    return result if isinstance(result, list) else []


async def get_client_registration_async(client_id):
    async with storage_session() as db:
        result = await ClientRegistration.handlers.list.core(
            {"payload": {"filters": {"client_id": client_id}}, "db": db}
        )
    rows = _items(result)
    return rows[0] if rows else None


async def get_latest_logout_for_session_async(session_id):
    async with storage_session() as db:
        return await LogoutState.handlers.latest_for_session.core(
            {"payload": {"session_id": session_id}, "db": db}
        )


async def terminate_session_async(session_id, **kwargs):
    async with storage_session() as db:
        session = await AuthSession.handlers.terminate.core(
            {"path_params": {"id": session_id}, "payload": kwargs, "db": db}
        )
        if session is None:
            return None
        return await LogoutState.handlers.ensure_for_session.core(
            {"payload": {"session_id": session_id, **kwargs}, "db": db}
        )


async def update_logout_metadata_async(logout_id, **kwargs):
    async with storage_session() as db:
        return await LogoutState.handlers.update_metadata.core(
            {
                "path_params": {"id": logout_id},
                "payload": {"logout_id": logout_id, **kwargs},
                "db": db,
            }
        )


async def mark_logout_channel_async(logout_id, **kwargs):
    async with storage_session() as db:
        return await LogoutState.handlers.mark_channel.core(
            {
                "path_params": {"id": logout_id},
                "payload": {"logout_id": logout_id, **kwargs},
                "db": db,
            }
        )


async def register_backchannel_replay_async(*, jti, issuer, client_id, expires_at, now):
    async with storage_session() as db:
        return await BackchannelLogoutReplay.handlers.register.core(
            {
                "payload": {
                    "jti": jti, "issuer": issuer, "client_id": str(client_id),
                    "expires_at": expires_at, "now": now,
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
