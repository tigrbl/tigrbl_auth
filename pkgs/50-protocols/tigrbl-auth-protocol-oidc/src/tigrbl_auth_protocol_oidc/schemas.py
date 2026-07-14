"""OpenID Connect wire schemas owned by the versioned protocol package."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class LogoutIn(BaseModel):
    id_token_hint: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None
    sid: str | None = None
    client_id: str | None = None


class LogoutOut(BaseModel):
    status: str
    session_id: str | None = None
    logout_id: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None
    cookie_cleared: bool = True
    cookie_policy: dict[str, Any] | None = None
    frontchannel_logout: dict[str, Any] | None = None
    backchannel_logout: dict[str, Any] | None = None
    replay_protected: bool = True


__all__ = ["LogoutIn", "LogoutOut"]
