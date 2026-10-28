"""tba_auth

Tigrbl-native authentication and authorization package checkpoint.

This package keeps top-level imports lightweight for governance and report
workflows while still exposing the dependency-light RFC helper surface expected
by the repository tests and previous checkpoints.
"""

from __future__ import annotations

import sys
from http import HTTPStatus as _HTTPStatus
from importlib import import_module
from typing import Any

from .compat import (
    FACADE_EXTRAS,
    STABLE_ENTRYPOINTS,
    FacadeImportError,
    StableEntrypoint,
    TbaAuthFacadeWarning,
    extras_for,
    resolve_entrypoint,
    stable_entrypoints,
    warn_legacy_import,
)


def _install_tomllib_alias() -> None:
    """Backfill ``tomllib`` on Python 3.10 using ``tomli`` if available."""

    if sys.version_info >= (3, 11):
        return
    try:  # pragma: no cover - exercised on Python 3.10 CI lanes
        import tomllib as _tomllib  # noqa: F401
    except ModuleNotFoundError:
        try:
            import tomli as _tomllib  # type: ignore[no-redef]
        except ModuleNotFoundError:
            return
        sys.modules.setdefault("tomllib", _tomllib)


def _install_http_status_aliases() -> None:
    """Provide Starlette-style ``HTTP_<code>_<NAME>`` aliases on ``HTTPStatus``.

    The repository tests and some release-path modules historically rely on the
    constant-style names exported by Starlette/FastAPI. Tigrbl uses the stdlib
    ``http.HTTPStatus`` enum, so install integer aliases once at package import
    time to keep both surfaces compatible.
    """

    for item in _HTTPStatus:
        alias = f"HTTP_{int(item)}_{item.name}"
        if not hasattr(_HTTPStatus, alias):
            setattr(_HTTPStatus, alias, int(item))


_install_tomllib_alias()
_install_http_status_aliases()

_MODULE_EXPORTS = {
    "cli": "tba_auth.cli",
    "compat": "tba_auth.compat",
    "identity_artifacts": "tba_auth.identity_artifacts",
    "config": "tba_auth.config",
    "profiles": "tba_auth.profiles",
    "runtime": "tba_auth.runtime",
    "runtime_cfg": "tba_auth.runtime_cfg",
    "security": "tba_auth.security",
    "services": "tba_auth.services",
    "standards": "tba_auth.standards",
    "uix": "tba_auth.uix",
    "rfc7591": "tba_auth.rfc.rfc7591",
    "rfc7592": "tba_auth.rfc.rfc7592",
    "rfc7662": "tba_auth.rfc.rfc7662",
    "rfc9101": "tba_auth.rfc.rfc9101",
}

_SYMBOL_EXPORTS = {
    "STANDARD_OWNER_MODULES": ("tba_runtime_identity", "STANDARD_OWNER_MODULES"),
    "RuntimeStandard": ("tba_runtime_identity", "RuntimeStandard"),
    "standard_version": ("tba_runtime_identity", "standard_version"),
    "standards_manifest": ("tba_runtime_identity", "standards_manifest"),
    "encode_jwt": ("tba_protocol_oauth.standards.json_web_token", "encode_jwt"),
    "decode_jwt": ("tba_protocol_oauth.standards.json_web_token", "decode_jwt"),
    "encrypt_jwe": ("tba_auth.standards.jose.rfc7516", "encrypt_jwe"),
    "decrypt_jwe": ("tba_auth.standards.jose.rfc7516", "decrypt_jwe"),
    "sign_jws": ("tba_auth.standards.jose.rfc7515", "sign_jws"),
    "verify_jws": ("tba_auth.standards.jose.rfc7515", "verify_jws"),
    "load_signing_jwk": ("tba_auth.standards.jose.rfc7517", "load_signing_jwk"),
    "load_public_jwk": ("tba_auth.standards.jose.rfc7517", "load_public_jwk"),
    "load_pqc_signing_jwk": (
        "tba_auth.standards.jose.rfc7517",
        "load_pqc_signing_jwk",
    ),
    "load_pqc_public_jwk": (
        "tba_auth.standards.jose.rfc7517",
        "load_pqc_public_jwk",
    ),
    "supported_algorithms": (
        "tba_auth.standards.jose.rfc7518",
        "supported_algorithms",
    ),
    "RFC7520_SPEC_URL": ("tba_auth.rfc.rfc7520", "RFC7520_SPEC_URL"),
    "jws_then_jwe": ("tba_auth.rfc.rfc7520", "jws_then_jwe"),
    "jwe_then_jws": ("tba_auth.rfc.rfc7520", "jwe_then_jws"),
    "makeCodeVerifier": (
        "tba_protocol_oauth.standards.proof_key_for_code_exchange",
        "makeCodeVerifier",
    ),
    "makeCodeChallenge": (
        "tba_protocol_oauth.standards.proof_key_for_code_exchange",
        "makeCodeChallenge",
    ),
    "verify_code_challenge": (
        "tba_protocol_oauth.standards.proof_key_for_code_exchange",
        "verify_code_challenge",
    ),
    "RFC8628_SPEC_URL": (
        "tba_protocol_oauth.standards.device_authorization",
        "RFC8628_SPEC_URL",
    ),
    "generate_user_code": (
        "tba_protocol_oauth.standards.device_authorization",
        "generate_user_code",
    ),
    "validate_user_code": (
        "tba_protocol_oauth.standards.device_authorization",
        "validate_user_code",
    ),
    "generate_device_code": (
        "tba_protocol_oauth.standards.device_authorization",
        "generate_device_code",
    ),
    "RFC9207_SPEC_URL": (
        "tba_protocol_oauth.standards.issuer_identification",
        "RFC9207_SPEC_URL",
    ),
    "extract_issuer": (
        "tba_protocol_oauth.standards.issuer_identification",
        "extract_issuer",
    ),
    "AuthorizationDetail": (
        "tba_protocol_oauth.standards.rich_authorization_requests",
        "AuthorizationDetail",
    ),
    "RFC9396_SPEC_URL": (
        "tba_protocol_oauth.standards.rich_authorization_requests",
        "RFC9396_SPEC_URL",
    ),
    "parse_authorization_details": (
        "tba_protocol_oauth.standards.rich_authorization_requests",
        "parse_authorization_details",
    ),
    "FACADE_EXTRAS": ("tba_auth.compat", "FACADE_EXTRAS"),
    "STABLE_ENTRYPOINTS": ("tba_auth.compat", "STABLE_ENTRYPOINTS"),
    "FacadeImportError": ("tba_auth.compat", "FacadeImportError"),
    "StableEntrypoint": ("tba_auth.compat", "StableEntrypoint"),
    "TbaAuthFacadeWarning": ("tba_auth.compat", "TbaAuthFacadeWarning"),
    "extras_for": ("tba_auth.compat", "extras_for"),
    "resolve_entrypoint": ("tba_auth.compat", "resolve_entrypoint"),
    "stable_entrypoints": ("tba_auth.compat", "stable_entrypoints"),
    "warn_legacy_import": ("tba_auth.compat", "warn_legacy_import"),
}


def __getattr__(name: str) -> Any:
    module_name = _MODULE_EXPORTS.get(name)
    if module_name is not None:
        module = import_module(module_name)
        globals()[name] = module
        return module
    symbol = _SYMBOL_EXPORTS.get(name)
    if symbol is not None:
        module_name, attr_name = symbol
        module = import_module(module_name)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_MODULE_EXPORTS) | set(_SYMBOL_EXPORTS))


__all__ = sorted(set(_MODULE_EXPORTS) | set(_SYMBOL_EXPORTS))
