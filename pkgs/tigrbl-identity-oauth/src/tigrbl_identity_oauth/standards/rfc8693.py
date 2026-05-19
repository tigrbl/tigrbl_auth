"""Compatibility facade for canonical RFC 8693 token-exchange helpers."""

from __future__ import annotations

from enum import Enum

from tigrbl_auth.standards.oauth2.token_exchange import (
    RFC8693_SPEC_URL,
    TOKEN_EXCHANGE_GRANT_TYPE,
    api,
    include_rfc8693,
    include_token_exchange_endpoint,
    router,
    token_exchange,
)


class TokenType(Enum):
    ACCESS_TOKEN = "urn:ietf:params:oauth:token-type:access_token"
    REFRESH_TOKEN = "urn:ietf:params:oauth:token-type:refresh_token"
    ID_TOKEN = "urn:ietf:params:oauth:token-type:id_token"
    SAML1 = "urn:ietf:params:oauth:token-type:saml1"
    SAML2 = "urn:ietf:params:oauth:token-type:saml2"
    JWT = "urn:ietf:params:oauth:token-type:jwt"


__all__ = [
    "RFC8693_SPEC_URL",
    "TOKEN_EXCHANGE_GRANT_TYPE",
    "TokenType",
    "api",
    "router",
    "token_exchange",
    "include_token_exchange_endpoint",
    "include_rfc8693",
]
