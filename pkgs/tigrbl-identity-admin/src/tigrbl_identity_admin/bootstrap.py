from __future__ import annotations

import hashlib
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from tigrbl_identity_server.framework import select
from tigrbl_identity_runtime.engine_resolver import resolve_api_provider
from tigrbl_identity_jose.key_management import hash_pw
from tigrbl_auth_protocol_oidc.standards.session_mgmt import resolve_browser_session
from tigrbl_identity_storage.tables import Tenant, User
from tigrbl_identity_storage.tables.engine import ENGINE


def _token_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def user_is_admin(user: User | None) -> bool:
    if user is None:
        return False
    return bool(getattr(user, "is_admin", False) or getattr(user, "is_superuser", False))


def _resolve_provider():
    try:
        from tigrbl_identity_server.api.surfaces import surface_api

        provider = resolve_api_provider(surface_api)
        if provider is not None:
            return provider
    except Exception:
        pass
    return ENGINE.provider


@asynccontextmanager
async def _session():
    provider = _resolve_provider()
    _, maker = provider.ensure()
    async with maker() as session:
        yield session


async def ensure_default_superuser_async(settings_obj: object) -> dict[str, str | bool] | None:
    username = str(getattr(settings_obj, "bootstrap_admin_username", "admin")).strip()
    email = str(getattr(settings_obj, "bootstrap_admin_email", "admin@example.com")).strip()
    tenant_slug = str(getattr(settings_obj, "bootstrap_admin_tenant_slug", "public")).strip()
    password = getattr(settings_obj, "bootstrap_admin_password", None)
    generated_password = False
    if not password:
        password = secrets.token_urlsafe(18)
        generated_password = True

    async with _session() as db:
        tenant = await db.scalar(select(Tenant).where(Tenant.slug == tenant_slug))
        if tenant is None:
            tenant = Tenant(slug=tenant_slug, name="Public", email="tenant@example.com")
            db.add(tenant)
            await db.flush()

        existing = await db.scalar(
            select(User).where((User.username == username) | (User.email == email))
        )
        if existing is not None:
            changed = False
            if not getattr(existing, "is_admin", False):
                existing.is_admin = True
                changed = True
            if not getattr(existing, "is_superuser", False):
                existing.is_superuser = True
                changed = True
            if getattr(existing, "tenant_id", None) != tenant.id:
                existing.tenant_id = tenant.id
                changed = True
            if changed:
                await db.commit()
            return None

        row = User(
            tenant_id=tenant.id,
            username=username,
            email=email,
            password_hash=hash_pw(str(password)),
            is_admin=True,
            is_superuser=True,
            must_change_password=bool(getattr(settings_obj, "bootstrap_admin_force_password_change", True)),
        )
        db.add(row)
        await db.commit()
        return {
            "username": username,
            "email": email,
            "password": str(password),
            "generated_password": generated_password,
        }


async def resolve_admin_user_from_request(request) -> User | None:
    session_row = await resolve_browser_session(request)
    if session_row is None:
        return None
    async with _session() as db:
        user = await db.scalar(select(User).where(User.id == session_row.user_id, User.is_active.is_(True)))
        if not user_is_admin(user):
            return None
        return user


async def issue_password_reset_token(*, user: User, minutes_valid: int = 15) -> str:
    token = secrets.token_urlsafe(32)
    async with _session() as db:
        row = await db.scalar(select(User).where(User.id == user.id))
        if row is None:
            raise ValueError("user not found")
        row.password_reset_token_hash = _token_digest(token)
        row.password_reset_expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes_valid)
        await db.commit()
    return token


async def consume_password_reset_token(*, token: str, new_password: str) -> User | None:
    digest = _token_digest(token)
    async with _session() as db:
        row = await db.scalar(select(User).where(User.password_reset_token_hash == digest))
        if row is None:
            return None
        expiry = getattr(row, "password_reset_expires_at", None)
        if expiry is None:
            return None
        effective_expiry = expiry if expiry.tzinfo is not None else expiry.replace(tzinfo=timezone.utc)
        if effective_expiry <= datetime.now(timezone.utc):
            return None
        row.password_hash = hash_pw(new_password)
        row.password_reset_token_hash = None
        row.password_reset_expires_at = None
        row.must_change_password = False
        await db.commit()
        return row


__all__ = [
    "consume_password_reset_token",
    "ensure_default_superuser_async",
    "issue_password_reset_token",
    "resolve_admin_user_from_request",
    "user_is_admin",
]
