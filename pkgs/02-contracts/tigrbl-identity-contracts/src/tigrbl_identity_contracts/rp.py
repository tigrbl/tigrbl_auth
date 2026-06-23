from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RPConfiguration:
    issuer: str
    client_id: str
    redirect_uri: str
    scopes: tuple[str, ...] = ("openid",)
    client_secret: str | None = None
    post_logout_redirect_uri: str | None = None

    def __post_init__(self) -> None:
        if not self.issuer or not self.client_id or not self.redirect_uri:
            raise ValueError("issuer, client_id, and redirect_uri are required")
        object.__setattr__(self, "issuer", self.issuer.rstrip("/"))
        object.__setattr__(self, "scopes", tuple(sorted(set(self.scopes))))


@dataclass(frozen=True, slots=True)
class LoginRequest:
    state: str
    nonce: str
    code_verifier: str
    redirect_uri: str
    scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CallbackResult:
    code: str
    state: str
    iss: str | None = None


@dataclass(frozen=True, slots=True)
class RPSession:
    subject: str
    id_token: str
    access_token: str
    refresh_token: str | None = None


__all__ = [
    "CallbackResult",
    "LoginRequest",
    "RPConfiguration",
    "RPSession",
]
