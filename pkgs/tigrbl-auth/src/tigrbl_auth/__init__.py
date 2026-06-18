"""tigrbl_auth

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
    TigrblAuthFacadeWarning,
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
    "api": "tigrbl_auth.api",
    "cli": "tigrbl_auth.cli",
    "compat": "tigrbl_auth.compat",
    "config": "tigrbl_auth.config",
    "framework": "tigrbl_auth.framework",
    "ops": "tigrbl_auth.ops",
    "profiles": "tigrbl_auth.profiles",
    "runtime": "tigrbl_auth.runtime",
    "runtime_cfg": "tigrbl_auth.runtime_cfg",
    "security": "tigrbl_auth.security",
    "services": "tigrbl_auth.services",
    "standards": "tigrbl_auth.standards",
    "uix": "tigrbl_auth.uix",
    "rfc7591": "tigrbl_auth.rfc.rfc7591",
    "rfc7592": "tigrbl_auth.rfc.rfc7592",
    "rfc7662": "tigrbl_auth.rfc.rfc7662",
    "rfc9101": "tigrbl_auth.rfc.rfc9101",
}

_SYMBOL_EXPORTS = {
    "encode_jwt": ("tigrbl_auth.standards.jose.rfc7519", "encode_jwt"),
    "decode_jwt": ("tigrbl_auth.standards.jose.rfc7519", "decode_jwt"),
    "encrypt_jwe": ("tigrbl_auth.standards.jose.rfc7516", "encrypt_jwe"),
    "decrypt_jwe": ("tigrbl_auth.standards.jose.rfc7516", "decrypt_jwe"),
    "sign_jws": ("tigrbl_auth.standards.jose.rfc7515", "sign_jws"),
    "verify_jws": ("tigrbl_auth.standards.jose.rfc7515", "verify_jws"),
    "load_signing_jwk": ("tigrbl_auth.standards.jose.rfc7517", "load_signing_jwk"),
    "load_public_jwk": ("tigrbl_auth.standards.jose.rfc7517", "load_public_jwk"),
    "load_pqc_signing_jwk": ("tigrbl_auth.standards.jose.rfc7517", "load_pqc_signing_jwk"),
    "load_pqc_public_jwk": ("tigrbl_auth.standards.jose.rfc7517", "load_pqc_public_jwk"),
    "supported_algorithms": ("tigrbl_auth.standards.jose.rfc7518", "supported_algorithms"),
    "RFC7520_SPEC_URL": ("tigrbl_auth.rfc.rfc7520", "RFC7520_SPEC_URL"),
    "jws_then_jwe": ("tigrbl_auth.rfc.rfc7520", "jws_then_jwe"),
    "jwe_then_jws": ("tigrbl_auth.rfc.rfc7520", "jwe_then_jws"),
    "makeCodeVerifier": ("tigrbl_auth.rfc.rfc7636_pkce", "makeCodeVerifier"),
    "makeCodeChallenge": ("tigrbl_auth.rfc.rfc7636_pkce", "makeCodeChallenge"),
    "verify_code_challenge": ("tigrbl_auth.rfc.rfc7636_pkce", "verify_code_challenge"),
    "RFC8628_SPEC_URL": ("tigrbl_auth.rfc.rfc8628", "RFC8628_SPEC_URL"),
    "generate_user_code": ("tigrbl_auth.rfc.rfc8628", "generate_user_code"),
    "validate_user_code": ("tigrbl_auth.rfc.rfc8628", "validate_user_code"),
    "generate_device_code": ("tigrbl_auth.rfc.rfc8628", "generate_device_code"),
    "RFC9207_SPEC_URL": ("tigrbl_auth.rfc.rfc9207", "RFC9207_SPEC_URL"),
    "extract_issuer": ("tigrbl_auth.rfc.rfc9207", "extract_issuer"),
    "AuthorizationDetail": ("tigrbl_auth.rfc.rfc9396", "AuthorizationDetail"),
    "RFC9396_SPEC_URL": ("tigrbl_auth.rfc.rfc9396", "RFC9396_SPEC_URL"),
    "parse_authorization_details": ("tigrbl_auth.rfc.rfc9396", "parse_authorization_details"),
    "RFC8932_SPEC_URL": ("tigrbl_auth.rfc.rfc8932", "RFC8932_SPEC_URL"),
    "enforce_encrypted_dns": ("tigrbl_auth.rfc.rfc8932", "enforce_encrypted_dns"),
    "FACADE_EXTRAS": ("tigrbl_auth.compat", "FACADE_EXTRAS"),
    "STABLE_ENTRYPOINTS": ("tigrbl_auth.compat", "STABLE_ENTRYPOINTS"),
    "FacadeImportError": ("tigrbl_auth.compat", "FacadeImportError"),
    "StableEntrypoint": ("tigrbl_auth.compat", "StableEntrypoint"),
    "TigrblAuthFacadeWarning": ("tigrbl_auth.compat", "TigrblAuthFacadeWarning"),
    "extras_for": ("tigrbl_auth.compat", "extras_for"),
    "resolve_entrypoint": ("tigrbl_auth.compat", "resolve_entrypoint"),
    "stable_entrypoints": ("tigrbl_auth.compat", "stable_entrypoints"),
    "warn_legacy_import": ("tigrbl_auth.compat", "warn_legacy_import"),
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
