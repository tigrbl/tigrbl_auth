from __future__ import annotations

import html
import secrets
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Iterable, Mapping


class OidcSessionStatus(str, Enum):
    ACTIVE = "active"
    LOGGED_OUT = "logged_out"
    EXPIRED = "expired"


class OidcProviderError(RuntimeError):
    pass


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _token(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(20)}"


@dataclass(frozen=True, slots=True)
class TenantBranding:
    tenant_id: str
    display_name: str
    logo_uri: str | None = None
    primary_color: str = "#111111"
    allowed_asset_prefixes: tuple[str, ...] = ("/assets/",)

    def sanitized_logo_uri(self) -> str | None:
        if not self.logo_uri:
            return None
        if not any(self.logo_uri.startswith(prefix) for prefix in self.allowed_asset_prefixes):
            raise OidcProviderError("logo URI is outside the tenant asset policy")
        return html.escape(self.logo_uri, quote=True)


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
        logo = branding.sanitized_logo_uri()
        escaped_name = html.escape(branding.display_name)
        escaped_client = html.escape(request.client_id)
        escaped_color = html.escape(branding.primary_color, quote=True)
        logo_markup = f'<img src="{logo}" alt="{escaped_name}">' if logo else ""
        rendered = (
            f'<main data-tenant="{html.escape(request.tenant_id)}" '
            f'data-client="{escaped_client}" style="--brand-color:{escaped_color}">'
            f"{logo_markup}<h1>{escaped_name}</h1>"
            '<form method="post" action="/login/complete">'
            f'<input type="hidden" name="state" value="{html.escape(request.state, quote=True)}">'
            f'<input type="hidden" name="nonce" value="{html.escape(request.nonce, quote=True)}">'
            "</form></main>"
        )
        return HostedLoginPage(
            tenant_id=request.tenant_id,
            client_id=request.client_id,
            html=rendered,
            state=request.state,
            nonce=request.nonce,
        )

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


__all__ = [
    "HostedLoginPage",
    "HostedLoginRequest",
    "LogoutPlan",
    "LogoutRequest",
    "OidcProviderError",
    "OidcProviderRuntime",
    "OidcSession",
    "OidcSessionStatus",
    "TenantBranding",
    "new_login_request",
]
