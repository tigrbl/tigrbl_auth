"""RFC 9068 access-token claim composition from standalone claim classes."""

from tigrbl_auth_protocol_jwt.claims import JWT_CLAIM_CLASSES
from tigrbl_auth_protocol_oauth.claims import OAUTH_EXTENSION_CLAIMS
from tigrbl_identity_contracts.claims import ClaimSet

RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES = tuple(
    dict.fromkeys((*JWT_CLAIM_CLASSES, *OAUTH_EXTENSION_CLAIMS))
)


def compose_access_token_claim_set(*claims: object) -> ClaimSet:
    unexpected = [
        getattr(claim, "name", type(claim).__name__)
        for claim in claims
        if not isinstance(claim, RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES)
    ]
    if unexpected:
        raise ValueError(
            f"claims are not valid RFC 9068 access-token claims: {unexpected}"
        )
    return ClaimSet(tuple(claims), "oauth-jwt-access-token", "RFC9068")


__all__ = [
    "RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES",
    "compose_access_token_claim_set",
]
