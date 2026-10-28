"""OAuth authorization-framework and extension specification revisions.

``VERSION_HISTORY`` is deliberately limited to the OAuth authorization
framework lineage. Extension RFCs have independent revision authority and
are recorded in ``EXTENSION_SPECIFICATIONS`` rather than being presented as
revisions of OAuth itself.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OAuthVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str


@dataclass(frozen=True, slots=True)
class OAuthExtensionSpecification:
    identifier: str
    title: str
    specification_uri: str


VERSION_HISTORY = (
    OAuthVersion(
        "RFC6749",
        "standards-track",
        "2012-10",
        "https://www.rfc-editor.org/rfc/rfc6749",
    ),
    OAuthVersion(
        "draft-ietf-oauth-v2-1-13",
        "superseded-draft-profile",
        "2025-05-28",
        "https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13",
    ),
    OAuthVersion(
        "draft-ietf-oauth-v2-1-14",
        "superseded-draft-profile",
        "2025-10-19",
        "https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-14",
    ),
    OAuthVersion(
        "draft-ietf-oauth-v2-1-15",
        "active-draft-profile",
        "2026-03-02",
        "https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-15",
    ),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def _extension(identifier: str, title: str) -> OAuthExtensionSpecification:
    return OAuthExtensionSpecification(
        identifier,
        title,
        f"https://www.rfc-editor.org/rfc/{identifier.lower()}",
    )


EXTENSION_SPECIFICATIONS = (
    _extension("RFC6750", "OAuth 2.0 Bearer Token Usage"),
    _extension("RFC7009", "OAuth 2.0 Token Revocation"),
    _extension("RFC7521", "Assertion Framework for OAuth 2.0"),
    _extension("RFC7523", "JWT Profile for OAuth 2.0 Client Authentication and Grants"),
    _extension("RFC7591", "OAuth 2.0 Dynamic Client Registration"),
    _extension("RFC7592", "OAuth 2.0 Dynamic Client Registration Management"),
    _extension("RFC7636", "Proof Key for Code Exchange"),
    _extension("RFC7662", "OAuth 2.0 Token Introspection"),
    _extension("RFC8252", "OAuth 2.0 for Native Apps"),
    _extension("RFC8414", "OAuth 2.0 Authorization Server Metadata"),
    _extension("RFC8628", "OAuth 2.0 Device Authorization Grant"),
    _extension("RFC8693", "OAuth 2.0 Token Exchange"),
    _extension(
        "RFC8705",
        "OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Tokens",
    ),
    _extension("RFC8707", "Resource Indicators for OAuth 2.0"),
    _extension("RFC8725", "JSON Web Token Best Current Practices"),
    _extension("RFC9068", "JWT Profile for OAuth 2.0 Access Tokens"),
    _extension("RFC9101", "JWT-Secured Authorization Request"),
    _extension("RFC9126", "OAuth 2.0 Pushed Authorization Requests"),
    _extension("RFC9207", "OAuth 2.0 Authorization Server Issuer Identification"),
    _extension("RFC9396", "OAuth 2.0 Rich Authorization Requests"),
    _extension("RFC9449", "OAuth 2.0 Demonstrating Proof of Possession"),
    _extension("RFC9700", "Best Current Practice for OAuth 2.0 Security"),
    _extension("RFC9728", "OAuth 2.0 Protected Resource Metadata"),
)


def select_version(
    identifier: str = "draft-ietf-oauth-v2-1-15",
) -> OAuthVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported OAuth version/profile: {identifier}")


__all__ = [
    "CURRENT_VERSION",
    "EXTENSION_SPECIFICATIONS",
    "VERSION_HISTORY",
    "OAuthExtensionSpecification",
    "OAuthVersion",
    "select_version",
]
