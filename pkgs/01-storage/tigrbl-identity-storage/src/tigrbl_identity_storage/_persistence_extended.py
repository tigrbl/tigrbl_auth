'Compatibility helpers for consent, registration, logout, and token records.'
from __future__ import annotations

from .persistence import *  # noqa: F401,F403
from .persistence import _created, _field, _items

async def record_consent_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    client_id: UUID,
    scope: str,
    claims: dict[str, Any] | None = None,
    expires_at: datetime | None = None,
) -> Consent:
    async with storage_session() as db:
        return await Consent.handlers.create.core(
            {
                "payload": {
                    "user_id": user_id,
                    "tenant_id": tenant_id,
                    "client_id": client_id,
                    "scope": scope,
                    "claims": claims,
                    "expires_at": expires_at,
                    "state": "active",
                },
                "db": db,
            }
        )


async def revoke_consent_async(consent_id: UUID) -> Consent | None:
    async with storage_session() as db:
        return await Consent.handlers.revoke_for_user.core(
            {"path_params": {"id": consent_id}, "payload": {"id": consent_id}, "db": db}
        )


def record_consent(**kwargs):
    return run_async(record_consent_async(**kwargs))


def revoke_consent(consent_id):
    return run_async(revoke_consent_async(consent_id))


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


async def upsert_token_record_async(
    token,
    claims=None,
    *,
    token_kind=None,
    token_type_hint=None,
    refresh_family_id=None,
    refresh_parent_hash=None,
    refresh_successor_hash=None,
    used_at=None,
    reuse_detected_at=None,
):
    digest = token_hash(token)
    async with storage_session() as db:
        await TokenRecord.handlers.persist_issued.core(
                {
                    "token_hash": digest,
                    "claims": dict(claims or {}),
                    "token_kind": token_kind,
                    "token_type_hint": token_type_hint,
                    "refresh_family_id": refresh_family_id,
                    "refresh_parent_hash": refresh_parent_hash,
                    "refresh_successor_hash": refresh_successor_hash,
                    "used_at": used_at,
                    "reuse_detected_at": reuse_detected_at,
                },
                db=db,
        )
    return digest


async def get_token_record_async(token):
    digest = token_hash(token)
    async with storage_session() as db:
        rows = _items(await TokenRecord.handlers.list.core({"payload": {"filters": {"token_hash": digest}}, "db": db}))
    return rows[0] if rows else None


async def remove_token_record_async(token):
    digest = token_hash(token)
    async with storage_session() as db:
        rows = _items(await TokenRecord.handlers.list.core({"payload": {"filters": {"token_hash": digest}}, "db": db}))
        if rows:
            await TokenRecord.handlers.delete.core({"path_params": {"id": getattr(rows[0], "id", None)}, "db": db})
    return None


async def mark_token_used_async(token, *, successor_token=None, reason="refresh_rotated"):
    digest = token_hash(token)
    successor_hash = token_hash(successor_token) if successor_token else None
    async with storage_session() as db:
        await TokenRecord.handlers.mark_rotated.core(
            {"token_hash": digest, "successor_hash": successor_hash, "reason": reason}, db=db
        )
    return digest


async def revoke_refresh_family_async(family_id, *, reason="refresh_token_reuse_detected", reuse_token=None):
    if not family_id:
        return 0
    reuse_hash = token_hash(reuse_token) if reuse_token else None
    async with storage_session() as db:
        rows = await TokenRecord.handlers.revoke_family.core(
            {"refresh_family_id": family_id, "reason": reason, "reuse_token_hash": reuse_hash}, db=db
        )
        for row in rows:
            await RevokedToken.handlers.record_hash.core(
                    {
                        "token_hash": getattr(row, "token_hash", None),
                        "token_type_hint": getattr(row, "token_type_hint", None),
                        "reason": reason,
                        "subject": getattr(row, "subject", None),
                        "tenant_id": getattr(row, "tenant_id", None),
                        "client_id": getattr(row, "client_id", None),
                        "expires_at": getattr(row, "expires_at", None),
                    },
                    db=db,
            )
    return len(rows)


async def introspect_token_async(token):
    digest = token_hash(token)
    try:
        async with storage_session() as db:
            if await RevokedToken.handlers.is_hash_revoked.core({"token_hash": digest}, db=db):
                return {"active": False}
            return await TokenRecord.handlers.introspect.core({"token_hash": digest}, db=db)
    except Exception:
        # Protocol adapters may provide an explicitly scoped fallback store (for
        # example, the RFC 7662 in-memory test adapter).  An unavailable or
        # unmigrated durable store therefore means "not found" at this boundary.
        return {"active": False}


introspect_token_record_async = introspect_token_async


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
    "is_revoked",
    "is_revoked_async",
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
