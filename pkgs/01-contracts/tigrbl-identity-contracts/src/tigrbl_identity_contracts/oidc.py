from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from .protocols import OidcSessionStatus

_HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


class OidcContractError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class LoginThemeAssetPolicy:
    allowed_asset_prefixes: tuple[str, ...] = ("/assets/",)
    allowed_image_extensions: tuple[str, ...] = (".svg", ".png", ".jpg", ".jpeg", ".webp")

    def validate_asset_uri(self, uri: str | None) -> str | None:
        if uri is None or uri == "":
            return None
        if not any(uri.startswith(prefix) for prefix in self.allowed_asset_prefixes):
            raise OidcContractError("logo URI is outside the tenant asset policy")
        lower = uri.lower()
        if not any(lower.endswith(extension) for extension in self.allowed_image_extensions):
            raise OidcContractError("logo URI extension is not allowed")
        if any(marker in uri for marker in ("..", "\\", "\x00", "\r", "\n")):
            raise OidcContractError("logo URI contains unsafe path characters")
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
            raise OidcContractError("tenant display name is required")
        return html.escape(value, quote=False)

    def sanitized_primary_color(self) -> str:
        if not _HEX_COLOR_RE.match(self.primary_color):
            raise OidcContractError("primary color must be a six-digit hex color")
        return html.escape(self.primary_color, quote=True)


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


@dataclass(frozen=True, slots=True)
class LogoutRequestContext:
    client_id: UUID | None
    post_logout_redirect_uri: str | None
    id_token_hint_claims: dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class SessionStateValidation:
    valid: bool
    reason: str
    origin: str
    presented_session_state: str | None
    expected_session_state: str | None


__all__ = [
    "HostedLoginPage",
    "HostedLoginRequest",
    "LoginThemeAssetPolicy",
    "LogoutPlan",
    "LogoutRequest",
    "LogoutRequestContext",
    "OidcContractError",
    "OidcSession",
    "SessionStateValidation",
    "TenantBranding",
]
