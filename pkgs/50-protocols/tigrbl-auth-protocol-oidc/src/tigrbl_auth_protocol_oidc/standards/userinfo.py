"""OIDC Core UserInfo specification ownership without runtime mounting."""

from __future__ import annotations

from typing import Final

from tigrbl_identity_core.standards import StandardOwner, describe_owner


OIDC_USERINFO_SPEC_URL: Final[str] = (
    "https://openid.net/specs/openid-connect-core-1_0.html#UserInfo"
)
USERINFO_SCOPE_CLAIMS: Final[dict[str, tuple[str, ...]]] = {
    "openid": ("sub",),
    "profile": ("name",),
    "email": ("email",),
    "address": ("address",),
    "phone": ("phone_number",),
}

OWNER = StandardOwner(
    label="OIDC Core UserInfo",
    title="OpenID Connect Core 1.0 UserInfo Endpoint",
    runtime_status="runtime-composed",
    public_surface=("/userinfo",),
    notes=(
        "Layer 50 owns the OIDC UserInfo version, scope-to-claim mapping, and "
        "wire semantics. Layer 60 composes verification and claim resolution; "
        "layer 80 owns the HTTP carrier.",
    ),
)


def describe() -> dict[str, object]:
    """Describe the selected OIDC Core UserInfo protocol feature."""

    return describe_owner(
        OWNER,
        specification_uri=OIDC_USERINFO_SPEC_URL,
        methods=("GET",),
        bearer_token_required=True,
        signed_response_media_type="application/jwt",
        scope_claims={
            scope: list(claims)
            for scope, claims in USERINFO_SCOPE_CLAIMS.items()
        },
    )


__all__ = [
    "OIDC_USERINFO_SPEC_URL",
    "OWNER",
    "USERINFO_SCOPE_CLAIMS",
    "describe",
]
