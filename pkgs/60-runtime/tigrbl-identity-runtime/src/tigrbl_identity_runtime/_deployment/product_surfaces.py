from __future__ import annotations

from typing import Any, Final

from .defaults import (
    all_surface_capability_registry,
    surface_route_registry,
)

PRODUCT_SURFACE_REGISTRY: Final[dict[str, dict[str, Any]]] = {
    "public-api": {
        "surface_sets": ("public-rest",),
        "allowed_capabilities": None,
        "admin_resources": (),
        "admin_rest_groups": (),
    },
    "platform-admin-api": {
        "surface_sets": ("admin-rest",),
        "allowed_capabilities": (),
        "admin_resources": (
            "Realm",
            "Tenant",
            "User",
            "AuditEvent",
            "CryptoKey",
            "CryptoKeyVersion",
            "PrincipalKeyBinding",
            "KeyEnvelope",
            "KeyAttestationEvidence",
            "KeyRotationEvent",
        ),
        "admin_rest_groups": ("admin_auth", "admin_realms", "admin_identities"),
    },
    "tenant-admin-api": {
        "surface_sets": ("admin-rest",),
        "allowed_capabilities": (),
        "admin_resources": (
            "User",
            "Client",
            "ClientRegistration",
            "Consent",
            "AuditEvent",
            "CryptoKey",
            "CryptoKeyVersion",
            "PrincipalKeyBinding",
            "KeyEnvelope",
            "KeyAttestationEvidence",
            "KeyRotationEvent",
        ),
        "admin_rest_groups": ("admin_auth", "admin_identities"),
    },
    "developer-api": {
        "surface_sets": ("public-rest", "admin-rest"),
        "allowed_capabilities": (
            "register",
            "register-management",
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "oauth-authorization-server-metadata",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
        ),
        "admin_resources": ("Client", "ClientRegistration", "AuditEvent"),
        "admin_rest_groups": (),
    },
    "service-admin-api": {
        "surface_sets": ("public-rest", "admin-rest"),
        "allowed_capabilities": (
            "introspection",
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "oauth-protected-resource-metadata",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
        ),
        "admin_resources": (
            "CredentialApiKey",
            "ServiceIdentity",
            "CredentialServiceKey",
            "TokenRecord",
            "AuditEvent",
        ),
        "admin_rest_groups": (),
    },
    "resource-validation-api": {
        "surface_sets": ("public-rest",),
        "allowed_capabilities": (
            "introspection",
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "oauth-protected-resource-metadata",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
        ),
        "admin_resources": (),
        "admin_rest_groups": (),
    },
    "my-account-api": {
        "surface_sets": ("public-rest",),
        "allowed_capabilities": (
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
            "account-profile",
            "account-sessions",
            "account-consents",
            "account-credentials",
        ),
        "admin_resources": (),
        "admin_rest_groups": (),
    },
}

PLUGIN_MODE_TO_SURFACE_SETS: Final[dict[str, tuple[str, ...]]] = {
    "public-only": ("public-rest",),
    "admin-only": ("admin-rest",),
    "mixed": ("public-rest", "admin-rest", "diagnostics"),
    "diagnostics-only": ("diagnostics",),
}

PROTOCOL_SLICE_REGISTRY: Final[dict[str, dict[str, Any]]] = {
    "device": {
        "flags": ("enable_rfc8628",),
        "routes": ("/device_authorization",),
        "targets": ("RFC 8628",),
    },
    "token-exchange": {
        "flags": ("enable_rfc8693",),
        "routes": ("/token/exchange",),
        "targets": ("RFC 8693",),
    },
    "par": {
        "flags": ("enable_rfc9126",),
        "routes": ("/par",),
        "targets": ("RFC 9126",),
    },
    "jar": {
        "flags": ("enable_rfc9101",),
        "routes": (),
        "targets": ("RFC 9101",),
    },
    "rar": {
        "flags": ("enable_rfc9396",),
        "routes": (),
        "targets": ("RFC 9396",),
    },
    "dpop": {
        "flags": ("enable_rfc9449",),
        "routes": (),
        "targets": ("RFC 9449",),
    },
    "mtls": {
        "flags": ("enable_rfc8705",),
        "routes": (),
        "targets": ("RFC 8705",),
    },
}

EXTENSION_REGISTRY: Final[dict[str, dict[str, Any]]] = {
    "webauthn-passkeys": {
        "flags": ("enable_rfc8812",),
        "targets": ("RFC 8812",),
        "boundary": "extension_quarantine",
    },
    "set": {
        "flags": ("enable_rfc7952",),
        "targets": ("RFC 7952",),
        "boundary": "extension_quarantine",
    },
    "webpush": {
        "flags": ("enable_rfc8291",),
        "targets": ("RFC 8291",),
        "boundary": "extension_quarantine",
    },
    "dns-privacy": {
        "flags": ("enable_rfc8932",),
        "targets": ("RFC 8932",),
        "boundary": "extension_quarantine",
    },
}

SURFACE_CAPABILITY_REGISTRY: Final[dict[str, dict[str, Any]]] = (
    all_surface_capability_registry()
)
ROUTE_REGISTRY: Final[dict[str, dict[str, Any]]] = surface_route_registry()

TARGET_FLAG_REQUIREMENTS: Final[dict[str, tuple[str, ...]]] = {
    "RFC 6749": ("enable_rfc6749", "surface_public_enabled"),
    "RFC 6750": ("enable_rfc6750", "surface_public_enabled"),
    "RFC 7636": ("enable_rfc7636", "surface_public_enabled"),
    "RFC 8414": ("enable_rfc8414", "surface_public_enabled"),
    "RFC 8615": ("enable_rfc8615", "surface_public_enabled"),
    "RFC 7515": ("enable_rfc7515", "surface_public_enabled"),
    "RFC 7516": ("enable_rfc7516", "surface_public_enabled"),
    "RFC 7517": ("enable_rfc7517", "surface_public_enabled"),
    "RFC 7518": ("enable_rfc7518", "surface_public_enabled"),
    "RFC 7519": ("enable_rfc7519", "surface_public_enabled"),
    "RFC 7009": ("enable_rfc7009", "surface_public_enabled"),
    "RFC 7521": ("enable_rfc7521", "surface_public_enabled"),
    "RFC 7523": ("enable_rfc7523", "surface_public_enabled"),
    "RFC 7591": ("enable_rfc7591", "surface_public_enabled"),
    "RFC 7592": ("enable_rfc7592", "surface_public_enabled"),
    "RFC 7662": ("enable_rfc7662", "surface_public_enabled"),
    "RFC 8252": ("enable_rfc8252", "surface_public_enabled"),
    "RFC 8628": ("enable_rfc8628", "surface_public_enabled"),
    "RFC 8693": ("enable_rfc8693", "surface_public_enabled"),
    "RFC 8705": ("enable_rfc8705", "surface_public_enabled"),
    "RFC 8707": ("enable_rfc8707", "surface_public_enabled"),
    "RFC 9068": ("enable_rfc9068", "surface_public_enabled"),
    "RFC 9101": ("enable_rfc9101", "surface_public_enabled"),
    "RFC 9126": ("enable_rfc9126", "surface_public_enabled"),
    "RFC 9207": ("enable_rfc9207", "surface_public_enabled"),
    "RFC 9396": ("enable_rfc9396", "surface_public_enabled"),
    "RFC 9449": ("enable_rfc9449", "surface_public_enabled"),
    "RFC 9700": ("enable_rfc9700", "surface_public_enabled"),
    "RFC 9728": ("enable_rfc9728", "surface_public_enabled"),
    "RFC 6265": ("enable_oidc_session_management", "surface_public_enabled"),
    "OIDC Core 1.0": ("enable_oidc_core", "surface_public_enabled"),
    "OIDC Discovery 1.0": ("enable_oidc_discovery", "surface_public_enabled"),
    "OIDC UserInfo": ("enable_oidc_userinfo", "surface_public_enabled"),
    "OIDC Session Management": (
        "enable_oidc_session_management",
        "surface_public_enabled",
    ),
    "OIDC RP-Initiated Logout": (
        "enable_oidc_rp_initiated_logout",
        "surface_public_enabled",
    ),
    "OIDC Front-Channel Logout": (
        "enable_oidc_frontchannel_logout",
        "surface_public_enabled",
    ),
    "OIDC Back-Channel Logout": (
        "enable_oidc_backchannel_logout",
        "surface_public_enabled",
    ),
    "OpenAPI 3.1 / 3.2 compatible public contract": ("surface_public_enabled",),
}


VALID_PROFILES: Final[tuple[str, ...]] = (
    "baseline",
    "baseline-development",
    "production",
    "hardening",
    "fapi2-security",
    "peer-claim",
)
VALID_PLUGIN_MODES: Final[tuple[str, ...]] = tuple(PLUGIN_MODE_TO_SURFACE_SETS)
VALID_RUNTIME_STYLES: Final[tuple[str, ...]] = ("plugin", "standalone")
VALID_PRODUCT_SURFACES: Final[tuple[str, ...]] = tuple(PRODUCT_SURFACE_REGISTRY)


