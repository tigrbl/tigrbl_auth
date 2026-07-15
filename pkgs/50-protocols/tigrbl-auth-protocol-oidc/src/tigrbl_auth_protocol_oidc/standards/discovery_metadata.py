"""Pure OpenID discovery metadata helpers.

The helpers in this module avoid importing the full framework/runtime stack so
profile-aware discovery snapshots can be generated during governance and
contract/reporting workflows.
"""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from tigrbl_identity_jose.standards.rfc7516 import jwe_policy_metadata
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
    token_endpoint_auth_methods_supported,
    token_endpoint_auth_signing_alg_values_supported,
)
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    SUPPORTED_MTLS_AUTH_METHODS,
)
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    ISSUER,
    JWKS_PATH,
)
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    discovery_policy_metadata,
)

OAUTH_PROTECTED_RESOURCE_PATH = "/.well-known/oauth-protected-resource"


class OidcDiscoveryDeployment(Protocol):
    """Runtime-neutral deployment view required by discovery projection."""

    issuer: str | None
    profile: str
    flags: Mapping[str, Any]
    active_capabilities: tuple[str, ...]

    def flag_enabled(self, flag: str) -> bool: ...

    def route_enabled(self, path: str) -> bool: ...

    def capability_enabled(self, capability: str) -> bool: ...


def build_openid_config(deployment: OidcDiscoveryDeployment) -> dict[str, Any]:
    """Project an injected deployment into OIDC discovery metadata."""
    issuer = str(deployment.issuer or ISSUER)
    scopes = ["openid", "profile", "email", "address", "phone"]
    claims = ["sub", "name", "email", "address", "phone_number"]
    auth_methods = token_endpoint_auth_methods_supported()
    if deployment.flag_enabled("enable_rfc8705") or deployment.profile in {
        "hardening",
        "fapi2-security",
        "peer-claim",
    }:
        auth_methods = list(
            dict.fromkeys([*auth_methods, *SUPPORTED_MTLS_AUTH_METHODS])
        )
    policy_metadata = discovery_policy_metadata(deployment)
    if "token_endpoint_auth_methods_supported" in policy_metadata:
        auth_methods = list(policy_metadata["token_endpoint_auth_methods_supported"])
    auth_signing_algs = token_endpoint_auth_signing_alg_values_supported()
    config: dict[str, Any] = {
        "issuer": issuer,
        "authorization_endpoint": f"{issuer}/authorize",
        "token_endpoint": f"{issuer}/token",
        "jwks_uri": f"{issuer}{JWKS_PATH}",
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"],
        "scopes_supported": scopes,
        "claims_supported": claims,
        "token_endpoint_auth_methods_supported": auth_methods,
    }
    if auth_signing_algs:
        config["token_endpoint_auth_signing_alg_values_supported"] = auth_signing_algs
    config.update(policy_metadata)
    if bool(
        deployment.flags.get("enable_oidc_userinfo", False)
    ) and deployment.route_enabled("/userinfo"):
        config["userinfo_endpoint"] = f"{issuer}/userinfo"
    if bool(deployment.flags.get("enable_id_token_encryption", False)):
        config.update(jwe_policy_metadata())
    if bool(deployment.flags.get("enable_rfc7591", False)) and deployment.route_enabled(
        "/register"
    ):
        config["registration_endpoint"] = f"{issuer}/register"
    if bool(deployment.flags.get("enable_rfc7009", False)) and deployment.route_enabled(
        "/revoke"
    ):
        config["revocation_endpoint"] = f"{issuer}/revoke"
        config["revocation_endpoint_auth_methods_supported"] = auth_methods
    if bool(deployment.flags.get("enable_rfc7662", False)) and deployment.route_enabled(
        "/introspect"
    ):
        config["introspection_endpoint"] = f"{issuer}/introspect"
        config["introspection_endpoint_auth_methods_supported"] = auth_methods
    if bool(
        deployment.flags.get("enable_oidc_rp_initiated_logout", False)
    ) and deployment.route_enabled("/logout"):
        config["end_session_endpoint"] = f"{issuer}/logout"
    if bool(
        deployment.flags.get("enable_oidc_frontchannel_logout", False)
    ) and deployment.route_enabled("/logout"):
        config["frontchannel_logout_supported"] = True
        config["frontchannel_logout_session_supported"] = True
    if bool(
        deployment.flags.get("enable_oidc_backchannel_logout", False)
    ) and deployment.route_enabled("/logout"):
        config["backchannel_logout_supported"] = True
        config["backchannel_logout_session_supported"] = True
    if bool(deployment.flags.get("enable_rfc8628", False)) and deployment.route_enabled(
        "/device_authorization"
    ):
        config["device_authorization_endpoint"] = f"{issuer}/device_authorization"
    if bool(deployment.flags.get("enable_rfc9126", False)) and deployment.route_enabled(
        "/par"
    ):
        config["pushed_authorization_request_endpoint"] = f"{issuer}/par"
    if bool(deployment.flags.get("enable_rfc9728", False)) and deployment.route_enabled(
        OAUTH_PROTECTED_RESOURCE_PATH
    ):
        config["protected_resource_metadata"] = (
            f"{issuer}{OAUTH_PROTECTED_RESOURCE_PATH}"
        )
    if (
        deployment.flag_enabled("enable_rfc8705")
        or deployment.profile == "fapi2-security"
    ):
        config["mtls_endpoint_aliases"] = {
            "token_endpoint": f"{issuer}/token",
            "revocation_endpoint": f"{issuer}/revoke",
            "introspection_endpoint": f"{issuer}/introspect",
            "registration_endpoint": f"{issuer}/register",
        }
    config["tigrbl_auth_capabilities"] = sorted(
        capability
        for capability in deployment.active_capabilities
        if deployment.capability_enabled(capability)
    )
    return config


__all__ = [
    "OAUTH_PROTECTED_RESOURCE_PATH",
    "OidcDiscoveryDeployment",
    "build_openid_config",
]
