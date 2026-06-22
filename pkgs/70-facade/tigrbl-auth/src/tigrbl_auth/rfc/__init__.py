"""Compatibility aliases for legacy RFC helper import paths."""

from __future__ import annotations

from tigrbl_auth._split_imports import alias_module as _alias_module


_LEGACY_NAME = __name__

_OAUTH_RFC_MODULES = (
    "rfc6749",
    "rfc6749_token",
    "rfc6750",
    "rfc7009",
    "rfc7521",
    "rfc7523",
    "rfc7519",
    "rfc7591",
    "rfc7592",
    "rfc7636_pkce",
    "rfc7662",
    "rfc7662_introspection",
    "rfc8252",
    "rfc8414",
    "rfc8414_metadata",
    "rfc8523",
    "rfc8628",
    "rfc8693",
    "rfc8705",
    "rfc8707",
    "rfc8725",
    "rfc9068",
    "rfc9101",
    "rfc9126",
    "rfc9207",
    "rfc9396",
    "rfc9449_dpop",
)
_JOSE_RFC_MODULES = (
    "rfc7515",
    "rfc7516",
    "rfc7517",
    "rfc7518",
    "rfc7520",
    "rfc7638",
    "rfc7800",
    "rfc8037",
    "rfc8176",
    "rfc8812",
)
_OAUTH_RFC_TARGETS = {
    "rfc6749": "authorization_framework",
    "rfc6749_token": "token_endpoint",
    "rfc6750": "bearer_token_usage",
    "rfc7009": "revocation",
    "rfc7519": "json_web_token",
    "rfc7521": "assertion_framework",
    "rfc7523": "jwt_client_auth",
    "rfc7591": "dynamic_client_registration",
    "rfc7592": "client_registration_management",
    "rfc7636_pkce": "proof_key_for_code_exchange",
    "rfc7662": "introspection",
    "rfc7662_introspection": "introspection",
    "rfc8252": "native_apps",
    "rfc8414": "authorization_server_metadata_endpoint",
    "rfc8414_metadata": "authorization_server_metadata",
    "rfc8523": "legacy_jwt_client_assertions",
    "rfc8628": "device_authorization",
    "rfc8693": "token_exchange",
    "rfc8705": "mutual_tls_client_authentication",
    "rfc8707": "resource_indicators",
    "rfc8725": "jwt_best_practices",
    "rfc9068": "jwt_access_tokens",
    "rfc9101": "jwt_secured_authorization_requests",
    "rfc9126": "pushed_authorization_requests",
    "rfc9207": "issuer_identification",
    "rfc9396": "rich_authorization_requests",
    "rfc9449_dpop": "dpop",
}

for _name in _OAUTH_RFC_MODULES:
    _alias_module(
        f"{_LEGACY_NAME}.{_name}",
        f"tigrbl_auth_protocol_oauth.standards.{_OAUTH_RFC_TARGETS.get(_name, _name)}",
        "tigrbl-auth-protocol-oauth",
    )

for _name in _JOSE_RFC_MODULES:
    _alias_module(
        f"{_LEGACY_NAME}.{_name}",
        f"tigrbl_identity_jose.standards.{_name}",
        "tigrbl-identity-jose",
    )

__all__ = sorted((*_OAUTH_RFC_MODULES, *_JOSE_RFC_MODULES))
