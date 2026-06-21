from __future__ import annotations

import html
import secrets
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterable, Mapping

from tigrbl_identity_contracts.oidc import (
    HostedLoginPage,
    HostedLoginRequest,
    LoginThemeAssetPolicy,
    LogoutPlan,
    LogoutRequest,
    OidcContractError,
    OidcSession,
    TenantBranding,
)
from tigrbl_identity_contracts.protocols import OidcSessionStatus


OidcProviderError = OidcContractError


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _token(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(20)}"


class TenantBrandingRegistry:
    def __init__(
        self,
        asset_policy: LoginThemeAssetPolicy | None = None,
    ) -> None:
        self.asset_policy = asset_policy or LoginThemeAssetPolicy()
        self._items: dict[str, TenantBranding] = {}

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


class OidcProviderRuntime:
    def __init__(
        self,
        allowed_redirect_uris: Mapping[str, tuple[str, ...]],
        frontchannel_logout_uris: Mapping[str, tuple[str, ...]] | None = None,
        backchannel_logout_uris: Mapping[str, tuple[str, ...]] | None = None,
        now: Callable[[], datetime] = _utc_now,
    ) -> None:
        self.allowed_redirect_uris = allowed_redirect_uris
        self.frontchannel_logout_uris = frontchannel_logout_uris or {}
        self.backchannel_logout_uris = backchannel_logout_uris or {}
        self.now = now
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
