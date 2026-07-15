"""Version ownership for the Tigrbl OAuth protected-resource profile."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProtectedResourceProfileVersion:
    identifier: str
    status: str
    published: str


@dataclass(frozen=True, slots=True)
class ProtectedResourceSpecification:
    identifier: str
    title: str
    specification_uri: str


VERSION_HISTORY = (
    ProtectedResourceProfileVersion(
        "tigrbl-oauth-protected-resource-1.0",
        "implementation-profile",
        "2026-07-15",
    ),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def _specification(
    identifier: str,
    title: str,
) -> ProtectedResourceSpecification:
    return ProtectedResourceSpecification(
        identifier,
        title,
        f"https://www.rfc-editor.org/rfc/{identifier.lower()}",
    )


SPECIFICATION_VERSIONS = (
    _specification("RFC6750", "OAuth 2.0 Bearer Token Usage"),
    _specification("RFC7662", "OAuth 2.0 Token Introspection"),
    _specification(
        "RFC8705",
        "OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Tokens",
    ),
    _specification("RFC9068", "JWT Profile for OAuth 2.0 Access Tokens"),
    _specification("RFC9449", "OAuth 2.0 Demonstrating Proof of Possession"),
    _specification("RFC9700", "Best Current Practice for OAuth 2.0 Security"),
    _specification("RFC9728", "OAuth 2.0 Protected Resource Metadata"),
)


def select_version(
    identifier: str = CURRENT_VERSION.identifier,
) -> ProtectedResourceProfileVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported protected-resource profile: {identifier}")


__all__ = [
    "CURRENT_VERSION",
    "SPECIFICATION_VERSIONS",
    "VERSION_HISTORY",
    "ProtectedResourceProfileVersion",
    "ProtectedResourceSpecification",
    "select_version",
]
