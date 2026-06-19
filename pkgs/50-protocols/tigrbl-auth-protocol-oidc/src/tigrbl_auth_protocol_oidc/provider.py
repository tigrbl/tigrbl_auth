from __future__ import annotations

import html
import re
import secrets
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from typing import Iterable, Mapping

from tigrbl_user_plane_contracts.protocols import OidcSessionStatus


class OidcProviderError(RuntimeError):
    pass


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _token(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(20)}"


_HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


@dataclass(frozen=True, slots=True)
class LoginThemeAssetPolicy:
    allowed_asset_prefixes: tuple[str, ...] = ("/assets/",)
    allowed_image_extensions: tuple[str, ...] = (".svg", ".png", ".jpg", ".jpeg", ".webp")

    def validate_asset_uri(self, uri: str | None) -> str | None:
        if uri is None or uri == "":
            return None
        if not any(uri.startswith(prefix) for prefix in self.allowed_asset_prefixes):
            raise OidcProviderError("logo URI is outside the tenant asset policy")
        lower = uri.lower()
        if not any(lower.endswith(extension) for extension in self.allowed_image_extensions):
            raise OidcProviderError("logo URI extension is not allowed")
        if any(marker in uri for marker in ("..", "\\", "\x00", "\r", "\n")):
            raise OidcProviderError("logo URI contains unsafe path characters")
        return html.escape(uri, quote=True)


@dataclass(frozen=True, slots=True)
class TenantBranding:
    tenant_id: str
    display_name: str
    logo_uri: str | None = None
    primary_color: str = "#111111"
    allowed_asset_prefixes: tuple[str, ...] = ("/assets/",)

    def sanitized_logo_uri(self) -> str | None:
        return LoginThemeAssetPolicy(self.allowed_asset_prefixes).validate_asset_uri(self.logo_uri)

    def sanitized_display_name(self) -> str:
        value = self.display_name.strip()
        if not value:
            raise OidcProviderError("tenant display name is required")
        return html.escape(value, quote=False)

    def sanitized_primary_color(self) -> str:
        if not _HEX_COLOR_RE.match(self.primary_color):
            raise OidcProviderError("primary color must be a six-digit hex color")
        return html.escape(self.primary_color, quote=True)


@dataclass(slots=True)
class TenantBrandingRegistry:
    asset_policy: LoginThemeAssetPolicy = field(default_factory=LoginThemeAssetPolicy)
    _items: dict[str, TenantBranding] = field(default_factory=dict, init=False, repr=False)

    def set(self, branding: TenantBranding) -> TenantBranding:
        self.asset_policy.validate_asset_uri(branding.logo_uri)
        branding.sanitized_display_name()
        branding.sanitized_primary_color()
        self._items[branding.tenant_id] = branding
        return branding

    def get(self, tenant_id: str) -> TenantBranding:
        try:
            return self._items[tenant_id]
        except KeyError as exc:
            raise OidcProviderError("tenant branding is not configured") from exc

    def snapshot(self) -> Mapping[str, TenantBranding]:
        return dict(self._items)


@dataclass(frozen=True, slots=True)
class HostedLoginRequest:
    tenant_id: str
    client_id: str
    redirect_uri: str
    scope: tuple[str, ...]
    state: str
    nonce: str


@dataclass(frozen=True, slots=True)
class HostedLoginPage:
    tenant_id: str
    client_id: str
    html: str
    state: str
    nonce: str
    asset_policy: LoginThemeAssetPolicy = field(default_factory=LoginThemeAssetPolicy)


@dataclass(frozen=True, slots=True)
class OidcSession:
    session_id: str
    tenant_id: str
    subject: str
    client_id: str
    nonce: str
    created_at: datetime
    expires_at: datetime
    status: OidcSessionStatus = OidcSessionStatus.ACTIVE


@dataclass(frozen=True, slots=True)
class LogoutRequest:
    tenant_id: str
    client_id: str
    session_id: str
    post_logout_redirect_uri: str | None = None
    state: str | None = None


@dataclass(frozen=True, slots=True)
class LogoutPlan:
    session_id: str
    status: OidcSessionStatus
    frontchannel_notifications: tuple[str, ...]
    backchannel_notifications: tuple[str, ...]
    redirect_uri: str | None
    state: str | None


@dataclass(slots=True)
class OidcProviderRuntime:
    allowed_redirect_uris: Mapping[str, tuple[str, ...]]
    frontchannel_logout_uris: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    backchannel_logout_uris: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    now: callable = field(default=_utc_now)
    _sessions: dict[str, OidcSession] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self._sessions = {}

    @property
    def sessions(self) -> Mapping[str, OidcSession]:
        return dict(self._sessions)

    def render_hosted_login(self, request: HostedLoginRequest, branding: TenantBranding) -> HostedLoginPage:
        self._require_redirect_uri(request.client_id, request.redirect_uri)
        if request.tenant_id != branding.tenant_id:
            raise OidcProviderError("tenant branding mismatch")
        if "openid" not in request.scope:
            raise OidcProviderError("OIDC hosted login requires openid scope")
        rendered = render_login_template(request, branding)
        return HostedLoginPage(
            tenant_id=request.tenant_id,
            client_id=request.client_id,
            html=rendered,
            state=request.state,
            nonce=request.nonce,
        )

    def render_hosted_login_for_tenant(
        self,
        request: HostedLoginRequest,
        registry: TenantBrandingRegistry,
    ) -> HostedLoginPage:
        return self.render_hosted_login(request, registry.get(request.tenant_id))

    def create_session(
        self,
        *,
        tenant_id: str,
        subject: str,
        client_id: str,
        nonce: str,
        ttl_seconds: int = 3600,
    ) -> OidcSession:
        if ttl_seconds <= 0:
            raise OidcProviderError("session ttl must be positive")
        session = OidcSession(
            session_id=_token("sid"),
            tenant_id=tenant_id,
            subject=subject,
            client_id=client_id,
            nonce=nonce,
            created_at=self.now(),
            expires_at=self.now() + timedelta(seconds=ttl_seconds),
        )
        self._sessions[session.session_id] = session
        return session

    def require_active_session(self, session_id: str) -> OidcSession:
        session = self._sessions.get(session_id)
        if session is None:
            raise OidcProviderError("unknown OIDC session")
        if session.status != OidcSessionStatus.ACTIVE:
            raise OidcProviderError("OIDC session is not active")
        if self.now() >= session.expires_at:
            expired = replace(session, status=OidcSessionStatus.EXPIRED)
            self._sessions[session_id] = expired
            raise OidcProviderError("OIDC session expired")
        return session

    def build_logout_plan(self, request: LogoutRequest) -> LogoutPlan:
        session = self.require_active_session(request.session_id)
        if session.tenant_id != request.tenant_id or session.client_id != request.client_id:
            raise OidcProviderError("logout request does not match OIDC session")
        if request.post_logout_redirect_uri is not None:
            self._require_redirect_uri(request.client_id, request.post_logout_redirect_uri)
        logged_out = replace(session, status=OidcSessionStatus.LOGGED_OUT)
        self._sessions[session.session_id] = logged_out
        return LogoutPlan(
            session_id=session.session_id,
            status=logged_out.status,
            frontchannel_notifications=tuple(self.frontchannel_logout_uris.get(request.client_id, ())),
            backchannel_notifications=tuple(self.backchannel_logout_uris.get(request.client_id, ())),
            redirect_uri=request.post_logout_redirect_uri,
            state=request.state,
        )

    def _require_redirect_uri(self, client_id: str, redirect_uri: str) -> None:
        allowed = self.allowed_redirect_uris.get(client_id, ())
        if redirect_uri not in allowed:
            raise OidcProviderError("redirect URI is not registered for client")


def new_login_request(
    *,
    tenant_id: str,
    client_id: str,
    redirect_uri: str,
    scopes: Iterable[str],
) -> HostedLoginRequest:
    return HostedLoginRequest(
        tenant_id=tenant_id,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=tuple(sorted(set(scopes))),
        state=_token("state"),
        nonce=_token("nonce"),
    )


def render_login_template(request: HostedLoginRequest, branding: TenantBranding) -> str:
    if request.tenant_id != branding.tenant_id:
        raise OidcProviderError("tenant branding mismatch")
    logo = branding.sanitized_logo_uri()
    escaped_name = branding.sanitized_display_name()
    escaped_tenant = html.escape(request.tenant_id, quote=True)
    escaped_client = html.escape(request.client_id, quote=True)
    escaped_redirect = html.escape(request.redirect_uri, quote=True)
    escaped_color = branding.sanitized_primary_color()
    escaped_scope = html.escape(" ".join(request.scope), quote=True)
    logo_markup = f'<img src="{logo}" alt="{escaped_name}">' if logo else ""
    return (
        f'<main data-tenant="{escaped_tenant}" data-client="{escaped_client}" '
        f'data-redirect-uri="{escaped_redirect}" style="--brand-color:{escaped_color}">'
        f"{logo_markup}<h1>{escaped_name}</h1>"
        '<form method="post" action="/login/complete" autocomplete="on">'
        f'<input type="hidden" name="state" value="{html.escape(request.state, quote=True)}">'
        f'<input type="hidden" name="nonce" value="{html.escape(request.nonce, quote=True)}">'
        f'<input type="hidden" name="scope" value="{escaped_scope}">'
        '<input name="identifier" autocomplete="username">'
        '<input name="password" type="password" autocomplete="current-password">'
        "</form></main>"
    )


__all__ = [
    "HostedLoginPage",
    "HostedLoginRequest",
    "LoginThemeAssetPolicy",
    "LogoutPlan",
    "LogoutRequest",
    "OidcProviderError",
    "OidcProviderRuntime",
    "OidcSession",
    "OidcSessionStatus",
    "TenantBranding",
    "TenantBrandingRegistry",
    "new_login_request",
    "render_login_template",
]
