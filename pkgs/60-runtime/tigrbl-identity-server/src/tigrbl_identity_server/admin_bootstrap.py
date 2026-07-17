from __future__ import annotations

import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

from tigrbl_identity_core.digests import sha256_text_digest
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.engine_resolver import (
    resolve_default_provider,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher
from tigrbl_identity_server.security.handler_records import (
    create_handler_record,
    first_handler_record,
    read_handler_record,
    resolve_browser_session_record,
    update_handler_record,
)
from tigrbl_identity_storage.tables import Realm, Tenant, User

DEFAULT_BOOTSTRAP_SUPERUSER_ID = "FFFFFFFF-0000-0000-0000-000000000001"
DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD = "AdminPass123!"


def user_is_admin(user: User | None) -> bool:
    if user is None:
        return False
    return bool(
        getattr(user, "is_admin", False) or getattr(user, "is_superuser", False)
    )


def _resolve_provider():
    provider = resolve_default_provider()
    if provider is None:
        raise RuntimeError("identity storage provider has not been configured")
    return provider


@asynccontextmanager
async def _session():
    provider = _resolve_provider()
    _, maker = provider.ensure()
    async with maker() as session:
        try:
            yield session
            commit = getattr(session, "commit", None)
            if callable(commit):
                result = commit()
                if hasattr(result, "__await__"):
                    await result
        except Exception:
            rollback = getattr(session, "rollback", None)
            if callable(rollback):
                result = rollback()
                if hasattr(result, "__await__"):
                    await result
            raise


async def _ensure_default_realm(db: Any) -> Realm:
    default_realm = dict(Realm.DEFAULT_ROWS[0])
    row = await first_handler_record(Realm, db, {"slug": default_realm["slug"]})
    if row is not None:
        return row
    return await create_handler_record(Realm, db, default_realm)


async def _ensure_default_tenant(db: Any, *, tenant_slug: str) -> Tenant:
    default_tenant = dict(Tenant.DEFAULT_ROWS[0])
    default_tenant["slug"] = tenant_slug
    realm = await _ensure_default_realm(db)
    default_tenant.setdefault("realm_id", realm.id)
    row = await first_handler_record(Tenant, db, {"slug": tenant_slug})
    if row is not None:
        return row
    return await create_handler_record(Tenant, db, default_tenant)


async def ensure_default_superuser_async(
    settings_obj: object,
) -> dict[str, str | bool] | None:
    username = str(getattr(settings_obj, "bootstrap_admin_username", "admin")).strip()
    email = str(
        getattr(settings_obj, "bootstrap_admin_email", "admin@example.com")
    ).strip()
    tenant_slug = str(
        getattr(settings_obj, "bootstrap_admin_tenant_slug", "public")
    ).strip()
    password = getattr(settings_obj, "bootstrap_admin_password", None)
    generated_password = False
    if not password:
        password = DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD

    async with _session() as db:
        tenant = await _ensure_default_tenant(db, tenant_slug=tenant_slug)
        existing = await first_handler_record(User, db, {"username": username})
        if existing is None:
            existing = await first_handler_record(User, db, {"email": email})
        if existing is not None:
            changes: dict[str, Any] = {}
            if not getattr(existing, "is_admin", False):
                changes["is_admin"] = True
            if not getattr(existing, "is_superuser", False):
                changes["is_superuser"] = True
            if getattr(existing, "tenant_id", None) != tenant.id:
                changes["tenant_id"] = tenant.id
            if changes:
                await update_handler_record(User, db, existing.id, changes)
            return None

        await create_handler_record(
            User,
            db,
            {
                "id": DEFAULT_BOOTSTRAP_SUPERUSER_ID,
                "tenant_id": tenant.id,
                "username": username,
                "email": email,
                "password_hash": BcryptSecretHasher()
                .hash_secret(str(password))
                .encoded,
                "is_admin": True,
                "is_superuser": True,
                "must_change_password": bool(
                    getattr(settings_obj, "bootstrap_admin_force_password_change", True)
                ),
                "is_active": True,
            },
        )
        return {
            "username": username,
            "email": email,
            "password": str(password),
            "generated_password": generated_password,
        }


async def resolve_admin_user_from_request(
    request, *, db: Any | None = None
) -> User | None:
    if db is None:
        async with _session() as session:
            return await resolve_admin_user_from_request(request, db=session)
    session_row = await resolve_browser_session_record(
        db,
        request,
        deployment=deployment_from_request(request, settings),
    )
    if session_row is None:
        return None
    user = await read_handler_record(User, db, session_row.user_id)
    if user is not None and not bool(getattr(user, "is_active", True)):
        user = None
    if not user_is_admin(user):
        return None
    return user


async def issue_password_reset_token(
    *, user: User, minutes_valid: int = 15, db: Any | None = None
) -> str:
    if db is None:
        async with _session() as session:
            return await issue_password_reset_token(
                user=user, minutes_valid=minutes_valid, db=session
            )
    token = secrets.token_urlsafe(32)
    row = await read_handler_record(User, db, user.id)
    if row is None:
        raise ValueError("user not found")
    await update_handler_record(
        User,
        db,
        row.id,
        {
            "password_reset_token_hash": sha256_text_digest(token),
            "password_reset_expires_at": datetime.now(timezone.utc)
            + timedelta(minutes=minutes_valid),
        },
    )
    return token


async def consume_password_reset_token(
    *, token: str, new_password: str, db: Any | None = None
) -> User | None:
    if db is None:
        async with _session() as session:
            return await consume_password_reset_token(
                token=token, new_password=new_password, db=session
            )
    digest = sha256_text_digest(token)
    row = await first_handler_record(User, db, {"password_reset_token_hash": digest})
    if row is None:
        return None
    expiry = getattr(row, "password_reset_expires_at", None)
    if expiry is None:
        return None
    effective_expiry = (
        expiry if expiry.tzinfo is not None else expiry.replace(tzinfo=timezone.utc)
    )
    if effective_expiry <= datetime.now(timezone.utc):
        return None
    return await update_handler_record(
        User,
        db,
        row.id,
        {
            "password_hash": BcryptSecretHasher().hash_secret(new_password).encoded,
            "password_reset_token_hash": None,
            "password_reset_expires_at": None,
            "must_change_password": False,
        },
    )


__all__ = [
    "DEFAULT_BOOTSTRAP_SUPERUSER_ID",
    "DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD",
    "consume_password_reset_token",
    "ensure_default_superuser_async",
    "issue_password_reset_token",
    "resolve_admin_user_from_request",
    "user_is_admin",
]
