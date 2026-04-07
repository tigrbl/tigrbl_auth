"""Canonical feature-flag registry for standards, surfaces, and operator UX."""

from __future__ import annotations

from typing import Final

FEATURE_FLAG_GROUPS: Final[dict[str, dict[str, object]]] = {
    "baseline": {
        "description": "Minimum interoperable OAuth 2.0 / OIDC / JOSE server targets.",
        "flags": {
            "enable_rfc6749": "RFC 6749 core authorization framework",
            "enable_rfc6750": "RFC 6750 bearer token usage",
            "enable_rfc7636": "RFC 7636 PKCE",
            "enable_rfc8414": "RFC 8414 authorization server metadata",
            "enable_rfc8615": "RFC 8615 .well-known naming",
            "enable_rfc7515": "RFC 7515 JWS",
            "enable_rfc7516": "RFC 7516 JWE",
            "enable_rfc7517": "RFC 7517 JWK / JWKS",
            "enable_rfc7518": "RFC 7518 JWA",
            "enable_rfc7519": "RFC 7519 JWT",
            "enable_oidc_core": "OIDC Core 1.0",
            "enable_oidc_discovery": "OIDC Discovery 1.0",
            "enable_oidc_session_management": "OIDC session management",
        },
    },
    "production": {
        "description": "Lifecycle, browser, registration, and metadata targets.",
        "flags": {
            "enable_rfc7009": "RFC 7009 revocation",
            "enable_rfc7521": "RFC 7521 assertion framework for authorization grants",
            "enable_rfc7523": "RFC 7523 JWT client authentication and authorization grants",
            "enable_rfc7662": "RFC 7662 introspection",
            "enable_rfc7591": "RFC 7591 dynamic client registration",
            "enable_rfc7592": "RFC 7592 registration management",
            "enable_rfc8252": "RFC 8252 native apps",
            "enable_rfc9068": "RFC 9068 JWT access-token profile",
            "enable_rfc9207": "RFC 9207 issuer identification",
            "enable_rfc9728": "RFC 9728 protected resource metadata",
            "enable_oidc_userinfo": "OIDC UserInfo",
            "enable_oidc_session_management": "OIDC session management",
            "enable_oidc_rp_initiated_logout": "OIDC RP-initiated logout",
        },
    },
    "hardening": {
        "description": "Advanced hardening and interoperability targets.",
        "flags": {
            "enable_rfc8628": "RFC 8628 device authorization",
            "enable_rfc8693": "RFC 8693 token exchange",
            "enable_rfc8705": "RFC 8705 mTLS",
            "enable_rfc8707": "RFC 8707 resource indicators",
            "enable_rfc9101": "RFC 9101 JAR",
            "enable_rfc9126": "RFC 9126 PAR",
            "enable_rfc9396": "RFC 9396 RAR",
            "enable_rfc9449": "RFC 9449 DPoP",
            "enable_rfc9700": "RFC 9700 security BCP alignment",
            "enable_oidc_frontchannel_logout": "OIDC front-channel logout",
            "enable_oidc_backchannel_logout": "OIDC back-channel logout",
        },
    },
    "operations": {
        "description": "Operational and security controls.",
        "flags": {
            "require_tls": "Require TLS for the public auth plane",
            "enable_id_token_encryption": "Enable encrypted ID Tokens",
            "enable_rfc6750_query": "Allow bearer tokens in query parameters",
            "enable_rfc6750_form": "Allow bearer tokens in form bodies",
            "strict_boundary_enforcement": "Fail closed on claim and boundary regressions",
        },
    },
    "surface": {
        "description": "Installable surface selection and partial feature consumption.",
        "flags": {
            "surface_public_enabled": "Mount public auth plane routes",
            "surface_admin_enabled": "Mount table-backed admin plane",
            "surface_operator_enabled": "Enable operator/governance plane",
            "surface_rpc_enabled": "Mount JSON-RPC control plane",
            "surface_diagnostics_enabled": "Attach diagnostics surface",
            "surface_plugin_mode": "Plugin install mode",
        },
    },
    "alignment_only": {
        "description": "Tracked alignment profiles that are never emitted as RFC claims.",
        "flags": {
            "oauth21_alignment_mode": "OAuth 2.1 alignment tracking mode",
        },
    },
    "extension_quarantine": {
        "description": "Flags outside the certified core boundary by default.",
        "flags": {
            "enable_rfc7800": "RFC 7800 proof-of-possession JWT semantics",
            "enable_rfc7952": "RFC 7952 SET",
            "enable_rfc8291": "RFC 8291 Web Push encryption",
            "enable_rfc8812": "RFC 8812 WebAuthn algorithm registrations",
            "enable_rfc8932": "RFC 8932 DNS privacy operator guidance",
            "enable_rfc8523": "Legacy mislabel retained for migration history only",
        },
    },
}

CLI_FLAG_GROUPS: Final[dict[str, dict[str, object]]] = {
    "global": {
        "description": "Shared operator flags",
        "flags": [
            "--config",
            "--env-file",
            "--profile",
            "--tenant",
            "--issuer",
            "--surface-set",
            "--slice",
            "--extension",
            "--plugin-mode",
            "--runtime-style",
            "--strict / --no-strict",
            "--offline",
            "--format",
            "--output",
            "--verbose",
            "--trace",
            "--color",
        ],
    },
    "serve": {
        "description": "Runtime serving surface",
        "flags": [
            "--environment",
            "--host",
            "--port",
            "--workers",
            "--surface-set",
            "--public / --no-public",
            "--admin / --no-admin",
            "--rpc / --no-rpc",
            "--diagnostics / --no-diagnostics",
            "--slice",
            "--extension",
            "--plugin-mode",
            "--runtime-style",
            "--proxy-headers",
            "--require-tls",
            "--enable-mtls",
            "--db-safe-start",
            "--jwks-refresh-seconds",
            "--cookies / --no-cookies",
            "--health / --no-health",
            "--metrics / --no-metrics",
            "--log-level",
        ],
    },
    "governance": {
        "description": "Certification and governance operators",
        "flags": [
            "spec",
            "verify",
            "gate",
            "evidence",
            "claims",
            "adr",
        ],
    },
    "admin": {
        "description": "Admin/operator resource surface",
        "flags": [
            "bootstrap",
            "migrate",
            "release",
            "tenant",
            "client",
            "identity",
            "flow",
            "session",
            "token",
            "key",
            "discovery",
            "import",
            "export",
        ],
    },
}

PROFILE_FLAG_SETS: Final[dict[str, tuple[str, ...]]] = {
    "baseline": tuple(FEATURE_FLAG_GROUPS["baseline"]["flags"].keys()),
    "production": tuple(
        list(FEATURE_FLAG_GROUPS["baseline"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["production"]["flags"].keys())
    ),
    "hardening": tuple(
        list(FEATURE_FLAG_GROUPS["baseline"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["production"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["hardening"]["flags"].keys())
    ),
    "fapi2-security": tuple(
        list(FEATURE_FLAG_GROUPS["baseline"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["production"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["hardening"]["flags"].keys())
    ),
    "peer-claim": tuple(
        list(FEATURE_FLAG_GROUPS["baseline"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["production"]["flags"].keys())
        + list(FEATURE_FLAG_GROUPS["hardening"]["flags"].keys())
    ),
}


def feature_flag_registry() -> dict[str, dict[str, object]]:
    return FEATURE_FLAG_GROUPS


def cli_flag_registry() -> dict[str, dict[str, object]]:
    return CLI_FLAG_GROUPS


def flags_for_profile(profile: str) -> tuple[str, ...]:
    return PROFILE_FLAG_SETS.get(profile, ())
