"""Runtime metadata route publishers for identity storage-backed surfaces."""

from .authorization_server_metadata import (
    RFC8414_SPEC_URL,
    include_rfc8414,
)
from .oidc_discovery import (
    ISSUER,
    JWKS_PATH,
    api as oidc_discovery_api,
    discovery_api,
    include_jwks,
    include_oidc_discovery,
    include_openid_configuration,
    jwks_api,
    refresh_discovery_cache,
)
from .protected_resource_metadata import (
    RFC9728_SPEC_URL,
    build_protected_resource_metadata,
    include_rfc9728,
)
from .resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
    include_resource_validation_metadata,
)

__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "ISSUER",
    "JWKS_PATH",
    "RFC8414_SPEC_URL",
    "RFC9728_SPEC_URL",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "build_protected_resource_metadata",
    "discovery_api",
    "include_jwks",
    "include_oidc_discovery",
    "include_openid_configuration",
    "include_resource_validation_metadata",
    "include_rfc8414",
    "include_rfc9728",
    "jwks_api",
    "oidc_discovery_api",
    "refresh_discovery_cache",
]
