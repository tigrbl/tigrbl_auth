from __future__ import annotations

from enum import Enum


class OAuthGrantStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    CONSUMED = "consumed"


class TokenType(Enum):
    ACCESS_TOKEN = "urn:ietf:params:oauth:token-type:access_token"
    REFRESH_TOKEN = "urn:ietf:params:oauth:token-type:refresh_token"
    ID_TOKEN = "urn:ietf:params:oauth:token-type:id_token"
    SAML1 = "urn:ietf:params:oauth:token-type:saml1"
    SAML2 = "urn:ietf:params:oauth:token-type:saml2"
    JWT = "urn:ietf:params:oauth:token-type:jwt"


class OidcSessionStatus(str, Enum):
    ACTIVE = "active"
    LOGGED_OUT = "logged_out"
    EXPIRED = "expired"


class BrowserStoragePolicy(str, Enum):
    MEMORY_ONLY = "memory_only"
    SESSION_STORAGE = "session_storage"
    LOCAL_STORAGE = "local_storage"


__all__ = [
    "BrowserStoragePolicy",
    "OAuthGrantStatus",
    "OidcSessionStatus",
    "TokenType",
]
