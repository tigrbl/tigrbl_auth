"""HTTP State Management Mechanism.

Domain-owned cookie policy and opaque browser-session cookie helpers for the
certified auth-core boundary.

This module intentionally keeps the cookie surface small:
- one opaque browser-session cookie
- secure / HttpOnly / SameSite enforcement from repository settings
- server-side validation against durable session state
- explicit cross-site handling when front/back-channel logout is enabled
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from http.cookies import SimpleCookie
import secrets
from typing import Final

from tigrbl_identity_core.standards import StandardOwner, describe_owner
from uuid import UUID

from tigrbl_identity_runtime.deployment import resolve_deployment
from tigrbl_identity_runtime.settings import settings

STATUS: Final[str] = "browser-session-runtime"
COOKIE_VALUE_VERSION: Final[str] = "v1"
DEFAULT_COOKIE_NAME: Final[str] = "sid"




@dataclass(frozen=True, slots=True)
class CookiePolicy:
    name: str
    path: str
    domain: str | None
    secure: bool
    http_only: bool
    same_site: str
    max_age_seconds: int
    cross_site: bool


@dataclass(frozen=True, slots=True)
class SessionCookieMaterial:
    session_id: UUID
    secret: str
    cookie_value: str


OWNER = StandardOwner(
    label="RFC 6265",
    title="HTTP State Management Mechanism",
    runtime_status=STATUS,
    public_surface=("/login", "/authorize", "/logout"),
    notes=(
        "Browser-session cookies are now domain-owned and opaque. The release path "
        "enforces secure / HttpOnly / SameSite policy, supports controlled cross-site "
        "mode for logout interoperability, and binds the cookie to durable session state."
    ),
)


def _normalize_same_site(value: str | None) -> str:
    raw = str(value or "lax").strip().lower()
    if raw not in {"lax", "strict", "none"}:
        return "lax"
    return raw


def _cross_site_enabled() -> bool:
    deployment = resolve_deployment(settings)
    return bool(settings.session_cookie_cross_site) or deployment.flag_enabled("enable_oidc_frontchannel_logout")


def session_cookie_policy(*, cross_site: bool | None = None) -> CookiePolicy:
    effective_cross_site = _cross_site_enabled() if cross_site is None else bool(cross_site)
    same_site = "none" if effective_cross_site else _normalize_same_site(settings.session_cookie_samesite)
    secure = bool(settings.require_tls or settings.session_cookie_force_secure or same_site == "none")
    return CookiePolicy(
        name=str(settings.session_cookie_name or DEFAULT_COOKIE_NAME),
        path=str(settings.session_cookie_path or "/"),
        domain=settings.session_cookie_domain or None,
        secure=secure,
        http_only=True,
        same_site=same_site,
        max_age_seconds=max(int(settings.session_cookie_max_age_seconds), 60),
        cross_site=effective_cross_site,
    )


def new_session_cookie_secret() -> str:
    return secrets.token_urlsafe(32)


def new_session_state_salt() -> str:
    return secrets.token_urlsafe(16)


def hash_cookie_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def build_session_cookie_value(session_id: UUID | str, secret: str) -> str:
    return f"{COOKIE_VALUE_VERSION}.{session_id}.{secret}"


def parse_session_cookie_value(value: str | None) -> SessionCookieMaterial | None:
    if not value or not isinstance(value, str):
        return None
    parts = value.split(".", 2)
    if len(parts) == 3:
        version, raw_session_id, secret = parts
        if version != COOKIE_VALUE_VERSION or not secret:
            return None
    else:
        raw_session_id = value
        secret = ""
    try:
        session_id = UUID(str(raw_session_id))
    except Exception:
        return None
    return SessionCookieMaterial(session_id=session_id, secret=secret, cookie_value=value)


def _expiry_delta(expires_at: datetime | None, max_age_seconds: int) -> int:
    if expires_at is None:
        return max_age_seconds
    effective = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
    seconds = int((effective - datetime.now(timezone.utc)).total_seconds())
    return max(seconds, 0)


def extract_session_cookie(request) -> str | None:
    name = session_cookie_policy().name
    cookies = getattr(request, "cookies", None)
    if cookies and hasattr(cookies, "get"):
        value = cookies.get(name)
        if value:
            return value
    headers = getattr(request, "headers", None) or {}
    raw_cookie = None
    header_sources = [headers]
    scope = getattr(request, "scope", None)
    if isinstance(scope, dict) and scope.get("headers") is not None:
        header_sources.append(scope["headers"])
    for header_source in header_sources:
        if hasattr(header_source, "get"):
            raw_cookie = header_source.get("cookie") or header_source.get("Cookie")
        if not raw_cookie:
            try:
                for key, value in header_source:
                    key_text = key.decode("latin-1") if isinstance(key, bytes) else str(key)
                    if key_text.lower() == "cookie":
                        raw_cookie = value.decode("latin-1") if isinstance(value, bytes) else str(value)
                        break
            except (TypeError, ValueError):
                raw_cookie = None
        if raw_cookie:
            break
    if not raw_cookie:
        return None
    parsed = SimpleCookie()
    try:
        parsed.load(str(raw_cookie))
    except Exception:
        return None
    morsel = parsed.get(name)
    return morsel.value if morsel is not None else None


def issue_session_cookie(
    response,
    *,
    session_id: UUID | str,
    secret: str,
    expires_at: datetime | None = None,
    cross_site: bool | None = None,
) -> None:
    policy = session_cookie_policy(cross_site=cross_site)
    max_age = _expiry_delta(expires_at, policy.max_age_seconds)
    response.set_cookie(
        policy.name,
        build_session_cookie_value(session_id, secret),
        max_age=max_age,
        path=policy.path,
        domain=policy.domain,
        secure=policy.secure,
        httponly=policy.http_only,
        samesite=policy.same_site,
    )


def clear_session_cookie(response, *, cross_site: bool | None = None) -> None:
    policy = session_cookie_policy(cross_site=cross_site)
    if hasattr(response, "delete_cookie"):
        response.delete_cookie(policy.name, path=policy.path, domain=policy.domain)
        return
    if hasattr(response, "set_cookie"):
        response.set_cookie(
            policy.name,
            "",
            max_age=0,
            path=policy.path,
            domain=policy.domain,
            secure=policy.secure,
            httponly=policy.http_only,
            samesite=policy.same_site,
        )
        return
    cookie_bits = [
        f"{policy.name}=",
        "Max-Age=0",
        f"Path={policy.path}",
        "HttpOnly",
        f"SameSite={policy.same_site}",
    ]
    if policy.domain:
        cookie_bits.append(f"Domain={policy.domain}")
    if policy.secure:
        cookie_bits.append("Secure")
    headers = getattr(response, "headers", None)
    if headers is not None:
        headers["set-cookie"] = "; ".join(cookie_bits)


def describe_runtime_policy() -> dict[str, object]:
    policy = session_cookie_policy()
    return describe_owner(
        OWNER,
        cookie_name=policy.name,
        path=policy.path,
        domain=policy.domain,
        secure=policy.secure,
        http_only=policy.http_only,
        same_site=policy.same_site,
        cross_site=policy.cross_site,
        max_age_seconds=policy.max_age_seconds,
        rotation_supported=True,
        invalidation_supported=True,
    )


def describe() -> dict[str, object]:
    return describe_runtime_policy()


__all__ = [
    "STATUS",
    "COOKIE_VALUE_VERSION",
    "DEFAULT_COOKIE_NAME",
    "CookiePolicy",
    "SessionCookieMaterial",
    "StandardOwner",
    "OWNER",
    "build_session_cookie_value",
    "clear_session_cookie",
    "describe",
    "describe_runtime_policy",
    "extract_session_cookie",
    "hash_cookie_secret",
    "issue_session_cookie",
    "new_session_cookie_secret",
    "new_session_state_salt",
    "parse_session_cookie_value",
    "session_cookie_policy",
]
